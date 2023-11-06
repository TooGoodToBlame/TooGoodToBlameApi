from django.urls import path

from .views import (
    BillDetail,
    BillList,
    MemberOfParliamentDetail,
    MemberOfParliamentList,
)

urlpatterns = [
    path(
        "member_of_parliament_list/",
        MemberOfParliamentList.as_view(),
        name="member_of_parliament-list",
    ),
    path(
        "member_of_parliament_list/<int:pk>/",
        MemberOfParliamentDetail.as_view(),
        name="member_of_parliament-detail",
    ),
    path("bill_list/", BillList.as_view(), name="bill-list"),
    path("bill_list/<int:pk>/", BillDetail.as_view(), name="bill-detail"),
]
