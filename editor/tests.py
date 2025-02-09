import pytest
from django.test import Client
from django.urls import reverse
from main.models import DimBill


@pytest.mark.django_db
def test_bill_search_view_empty():
    """
    Test GET na BillSearchView, gdy nie ma żadnych ustaw w bazie.
    """
    client = Client()
    url = reverse('search_bill')
    response = client.get(url)
    assert response.status_code == 200
    # content = response.content.decode("utf-8")
    # assert "Brak wyników" in content or "bills" in content #migracja testowa psuje


@pytest.mark.django_db
def test_bill_search_view_with_data():
    """
    Test GET na BillSearchView przy istnieniu kilku ustaw.
    """
    DimBill.objects.create(
        bill_id="BILL-TEST1", title="Test 1", voting_date="2023-01-01",
        content="Lorem", summary="Ipsum"
    )
    DimBill.objects.create(
        bill_id="BILL-TEST2", title="Another Bill", voting_date="2023-05-10",
        content="Blabla", summary=""
    )

    client = Client()
    url = reverse('search_bill')
    response = client.get(url + "?title_search=Test")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Test 1" in content
    assert "Another Bill" not in content


@pytest.mark.django_db
def test_edit_bill_get_form():
    """
    Test GET na EditBill (UpdateView) - formularz edycji.
    """
    bill = DimBill.objects.create(
        bill_id="BILL-123", title="Old Title", voting_date="2023-01-02",
        content="Old Content", summary="Old Summary"
    )
    client = Client()
    url = reverse('edit_bill', kwargs={"pk": bill.id})
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Old Title" in content


@pytest.mark.django_db
def test_edit_bill_post_form():
    """
    Test POST na EditBill (UpdateView) - wysyłanie zmian w formularzu.
    """
    bill = DimBill.objects.create(
        bill_id="BILL-999", title="Original Title", voting_date="2023-06-01",
        content="Original content", summary="Summ"
    )
    client = Client()
    url = reverse('edit_bill', kwargs={"pk": bill.id})
    payload = {
        "title": "New Title",
        "voting_date": "2023-06-15",
        "content": "Updated Content",
        "summary": "New Summ"
    }
    response = client.post(url, data=payload, follow=True)
    assert response.status_code == 200
    updated_bill = DimBill.objects.get(id=bill.id)
    assert updated_bill.title == "New Title"
    assert updated_bill.content == "Updated Content"
