from django_filters import rest_framework as django_filters
from rest_framework import filters, generics

from .models import Bill, MemberOfParliament, PARTIES, REGIONS
from .serializers import (
    BillListSerializer,
    BillSerializer,
    MemberOfParliamentSerializer,
)

# class MemberOfParliamentList(APIView):
#     def get(self, request):
#         # poslowie = MemberOfParliament.objects.all().order_by('party', 'last_name')
#         poslowie = MemberOfParliament.objects.all()
#         data = {}

#         for member_of_parliament in poslowie:
#             if member_of_parliament.party not in data:
#                 data[member_of_parliament.party] = []

#             serialized = MemberOfParliamentSerializer(member_of_parliament).data
#             data[member_of_parliament.party].append(serialized)

#         return JsonResponse(data)

from rest_framework import filters

# class MemberOfParliamentList(generics.ListAPIView):
#     queryset = MemberOfParliament.objects.all()
#     serializer_class = MemberOfParliamentSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["region"]
#     ordering_fields = ["party", "number_on_list"]

#     party = django_filters.CharFilter(field_name="party")
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         filtered_queryset = self.filter_queryset(queryset)
#         print(filtered_queryset.query)  # Wydrukuj zapytanie SQL do konsoli
#         return filtered_queryset



from django_filters import rest_framework as django_filters
from rest_framework import filters

# Upewnij się, że zdefiniowałeś tę klasę w pliku filters.py lub gdzieś, gdzie jest importowana.
class MemberOfParliamentFilter(django_filters.FilterSet):
    party = django_filters.ChoiceFilter(choices=PARTIES)
    region = django_filters.ChoiceFilter(choices=REGIONS)
    # party = django_filters.ChoiceFilter()
    # region = django_filters.ChoiceFilter()

    class Meta:
        model = MemberOfParliament
        fields = ['party', 'region']

# Ta klasa powinna być w views.py lub gdzieś, gdzie jest importowana.
class MemberOfParliamentList(generics.ListAPIView):
    queryset = MemberOfParliament.objects.all()
    serializer_class = MemberOfParliamentSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MemberOfParliamentFilter  # Ustaw klasę filtrów
    search_fields = ["first_name", "last_name"]  # Możesz dodać więcej pól do wyszukiwania
    ordering_fields = ["party", "number_on_list"]
    ordering = ["party", "last_name"]  # Domyślne sortowanie



    # Metoda get_queryset może zostać dostosowana, jeśli potrzebujesz bardziej złożonej logiki filtrowania

# class MemberOfParliamentList(generics.ListAPIView):
#     queryset = MemberOfParliament.objects.all().order_by("party", "last_name")
#     serializer_class = MemberOfParliamentSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["region"]


class MemberOfParliamentDetail(generics.RetrieveAPIView):
    queryset = MemberOfParliament.objects.all()
    serializer_class = MemberOfParliamentSerializer


class BillDetail(generics.RetrieveAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

class BillFilter(django_filters.FilterSet):
    member_of_parliament = django_filters.NumberFilter(field_name="vote__member_of_parliament__id")
    member_of_parliament_name = django_filters.CharFilter(method='filter_member_of_parliament_name')

    class Meta:
        model = Bill
        fields = []

    def filter_member_of_parliament_name(self, queryset, name, value):
        return queryset.distinct().filter(vote__member_of_parliament__first_name__icontains=value) | \
            queryset.distinct().filter(vote__member_of_parliament__last_name__icontains=value)

class BillList(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillListSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BillFilter
    ordering_fields = ["id", "voting_date", "summary", "title"]
    ordering = ["voting_date"]

    def get_queryset(self):
        queryset = Bill.objects.all()
        member_of_parliament = self.request.query_params.get('member_of_parliament')
        if member_of_parliament is not None:
            queryset = queryset.filter(vote__member_of_parliament__id=member_of_parliament)
        return queryset.distinct()
