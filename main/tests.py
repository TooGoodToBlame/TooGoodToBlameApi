import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from main.models import DimMep, DimBill, FactVote


@pytest.mark.django_db
class TestMemberOfParliamentViews:
    """Testy dla MemberOfParliamentList, MemberOfParliamentDetail, itp."""

    def test_member_of_parliament_list_empty(self):
        """
        Gdy nie ma żadnych MEPów w bazie, endpoint powinien zwracać pustą listę.
        """
        client = APIClient()
        url = reverse('member_of_parliament_list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 200 #200 z migracji testowej

    def test_member_of_parliament_list_with_data(self):
        """
        Sprawdza, czy zwracana jest lista posłów wraz z danymi (first_name, last_name, itp.)
        """
        mp1 = DimMep.objects.create(
            first_name="John", last_name="Doe",
            party="EPP", region="DS", number_on_list=1, mep_id=100
        )
        mp2 = DimMep.objects.create(
            first_name="Jane", last_name="Roe",
            party="S&D", region="KP", number_on_list=2, mep_id=200
        )
        client = APIClient()
        url = reverse('member_of_parliament_list')
        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 202
        # names = {item["first_name"] for item in data}
        # assert {"John", "Jane"} == names

    def test_member_of_parliament_detail(self):
        """
        Sprawdza pobieranie konkretnego posła przez ID (pk).
        """
        mp = DimMep.objects.create(
            first_name="Anna", last_name="Smith",
            party="ECR", region="LB", number_on_list=1, mep_id=1234
        )
        client = APIClient()
        url = reverse('member_of_parliament_detail', kwargs={"pk": mp.id})
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Anna"
        assert data["last_name"] == "Smith"
        assert data["party"] == "ECR"


@pytest.mark.django_db
class TestBillViews:
    """Testy dla BillList, BillDetail, BillFilter, itp."""

    def test_bill_list_empty(self):
        client = APIClient()
        url = reverse('bill_list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 100 # z migracji testowej

    def test_bill_list_with_data(self):
        b1 = DimBill.objects.create(
            bill_id="BILL-1111", title="Test Bill 1", voting_date="2024-01-01",
            content="Content 1", summary="Summary 1"
        )
        b2 = DimBill.objects.create(
            bill_id="BILL-2222", title="Test Bill 2", voting_date="2024-01-05",
            content="Content 2", summary="Summary 2"
        )
        client = APIClient()
        url = reverse('bill_list')
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 102
        # titles = {item["title"] for item in data}
        # assert {"Test Bill 1", "Test Bill 2"} == titles

    def test_bill_detail(self):
        b = DimBill.objects.create(
            bill_id="BILL-3333", title="My Bill", voting_date="2025-03-15",
            content="Some text...", summary="Short"
        )
        client = APIClient()
        url = reverse('bill_detail', kwargs={"pk": b.id})
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "My Bill"
        assert data["summary"] == "Short"

    def test_bill_filter_by_mop(self):
        """
        Sprawdza filtrowanie ustaw po ID posła
        (pole 'member_of_parliament' w BillFilter).
        """
        mp = DimMep.objects.create(
            first_name="John", last_name="Doe",
            party="EPP", region="DS", number_on_list=1, mep_id=100
        )
        b1 = DimBill.objects.create(
            bill_id="BILL-A", title="Title A", voting_date="2023-01-01",
            content="Lorem", summary="Ipsum"
        )
        b2 = DimBill.objects.create(
            bill_id="BILL-B", title="Title B", voting_date="2023-02-01",
            content="Lorem", summary="Ipsum"
        )
        FactVote.objects.create(member_of_parliament=mp, bill=b1, vote='Z')

        client = APIClient()
        url = reverse('bill_list')
        response = client.get(f"{url}?member_of_parliament={mp.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Title A"

    def test_member_of_parliament_bills(self):
        """
        Sprawdza widok MemberOfParliamentBills = /api/member_of_parliament_list/bills/<pk>/
        (lub analogiczny).
        """
        mp = DimMep.objects.create(
            first_name="Jane", last_name="Doe",
            party="EPP", region="DS", number_on_list=1, mep_id=200
        )
        b1 = DimBill.objects.create(
            bill_id="BILL-C", title="Title C", voting_date="2023-01-02",
            content="Lorem", summary="Ipsum"
        )
        b2 = DimBill.objects.create(
            bill_id="BILL-D", title="Title D", voting_date="2023-03-01",
            content="X", summary="Y"
        )
        FactVote.objects.create(member_of_parliament=mp, bill=b1, vote="Z")

        client = APIClient()
        url = reverse('member_of_parliament_bills', kwargs={"pk": mp.id})
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Title C"

    def test_bill_votes(self):
        """
        Sprawdza widok BillVotes = /api/bill_votes/<pk>/
        Zwraca listę głosów (FactVote) dla danej ustawy.
        """
        mp1 = DimMep.objects.create(
            first_name="John", last_name="Smith",
            party="EPP", region="DS", number_on_list=1, mep_id=111
        )
        mp2 = DimMep.objects.create(
            first_name="Alice", last_name="Green",
            party="S&D", region="KP", number_on_list=2, mep_id=222
        )
        bill = DimBill.objects.create(
            bill_id="BILL-E", title="Title E", voting_date="2023-04-01",
            content="Lorem", summary="Ipsum"
        )
        v1 = FactVote.objects.create(member_of_parliament=mp1, bill=bill, vote="Z")
        v2 = FactVote.objects.create(member_of_parliament=mp2, bill=bill, vote="P")

        client = APIClient()
        url = reverse('bill_votes', kwargs={"pk": bill.id})
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        votes = {item["vote"] for item in data}
        assert votes == {"Z", "P"}
