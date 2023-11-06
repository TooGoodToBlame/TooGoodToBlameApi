from django.urls import path

from .views import BillSearchView, EditBill

urlpatterns = [
    path("search/", BillSearchView.as_view(), name="search_bill"),
    path("edit-bill/<int:pk>/", EditBill.as_view(), name="edit_bill"),
]
