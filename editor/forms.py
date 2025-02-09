from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout
from django import forms

from main.models import DimBill as Bill


class BillSearchForm(forms.Form):
    has_summary = forms.ChoiceField(
        choices=[("", "-----"), (True, "Has Summary"), (False, "No Summary")],
        required=False,
    )
    title_search = forms.CharField(
        max_length=255, required=False, label="Search by Title"
    )
    date_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    date_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill 
        fields = ["title", "voting_date", "content", "summary"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["voting_date"] = forms.DateField(
            widget=forms.TextInput(attrs={"type": "date"})
        )
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(HTML("form"), css_class="card-header"),
                    "title",
                    "voting_date",
                    Field("content", css_class="text-input text-area"),
                    Field("summary", css_class="text-input text-area"),
                    css_class="card-body",
                )
            )
        )
