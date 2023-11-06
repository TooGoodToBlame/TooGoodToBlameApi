from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView

from main.models import Bill

from .forms import BillForm, BillSearchForm

class BillSearchView(View):
    template_name = "search_bill.html"
    form_class = BillSearchForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)
        bills = Bill.objects.all()

        if form.is_valid():
            if form.cleaned_data["has_summary"]:
                has_summary = form.cleaned_data["has_summary"] == "True"
                bills = bills.filter(summary__isnull=not has_summary)
            if form.cleaned_data["title_search"]:
                bills = bills.filter(title__icontains=form.cleaned_data["title_search"])
            if form.cleaned_data["date_from"]:
                bills = bills.filter(voting_date__gte=form.cleaned_data["date_from"])
            if form.cleaned_data["date_to"]:
                bills = bills.filter(voting_date__lte=form.cleaned_data["date_to"])

        context = {"form": form, "bills": bills}
        return render(request, self.template_name, context)


class EditBill(UpdateView):
    model = Bill
    form_class = BillForm
    template_name = "edit_bill.html"
    success_url = reverse_lazy("search_bill")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Edytuj Bill {self.object.id}"
        return context
