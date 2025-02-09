from django.db.models import Q
from django_filters import rest_framework as django_filters
from rest_framework import filters, generics

from .models import PARTIES, REGIONS, Bill, MemberOfParliament, Vote
from .serializers import (
    BillListSerializer,
    BillSerializer,
    MemberOfParliamentSerializer,
    BillWithMPVoteSerializer,
    VoteSerializer,
)

class MemberOfParliamentFilter(django_filters.FilterSet):
    party = django_filters.ChoiceFilter(choices=PARTIES)
    region = django_filters.ChoiceFilter(choices=REGIONS)

    class Meta:
        model = MemberOfParliament
        fields = ["party", "region"]


class MemberOfParliamentList(generics.ListAPIView):
    queryset = MemberOfParliament.objects.all()
    serializer_class = MemberOfParliamentSerializer
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = MemberOfParliamentFilter
    ordering_fields = ["party", "number_on_list"]
    ordering = ["party", "last_name"]


class MemberOfParliamentDetail(generics.RetrieveAPIView):
    queryset = MemberOfParliament.objects.all()
    serializer_class = MemberOfParliamentSerializer

class BillFilter(django_filters.FilterSet):
    member_of_parliament = django_filters.NumberFilter(
        field_name="vote__member_of_parliament__id",
        label='MOP_id'
    )
    member_of_parliament_name = django_filters.CharFilter(
        method="filter_member_of_parliament_name",
        label='MOP_name'
    )

    class Meta:
        model = Bill
        fields = []

    def filter_member_of_parliament_name(self, queryset, name, value):
        return queryset.filter(
            Q(vote__member_of_parliament__first_name__icontains=value) |
            Q(vote__member_of_parliament__last_name__icontains=value)
        )


class BillList(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillListSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BillFilter
    ordering_fields = ["id", "voting_date", "title"]
    ordering = ["voting_date"]

    def get_queryset(self):
        queryset = Bill.objects.all()
        member_of_parliament = self.request.query_params.get("member_of_parliament")
        if member_of_parliament is not None:
            queryset = queryset.filter(
                vote__member_of_parliament__id=member_of_parliament
            )
        return queryset.distinct()


class BillDetail(generics.RetrieveAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class MemberOfParliamentBills(generics.ListAPIView):
    serializer_class = BillWithMPVoteSerializer

    def get_queryset(self):
        mp_id = self.kwargs["pk"]
        return Bill.objects.filter(
            vote__member_of_parliament_id=mp_id
        ).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["mp_id"] = self.kwargs["pk"]
        return context


class BillVotes(generics.ListAPIView):
    serializer_class = VoteSerializer

    def get_queryset(self):
        bill_id = self.kwargs["pk"]
        return Vote.objects.filter(bill_id=bill_id)
