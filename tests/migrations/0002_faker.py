import random
from collections import defaultdict
from uuid import uuid4  # Poprawka: Importowanie poprawnego generatora UUID

from django.db import migrations
from faker import Faker

from main.models import PARTIES, REGIONS, VOTES


def generate_data(apps, schema_editor):
    """
    Funkcja wykonująca się podczas migracji 'forward':
      - Dodaje losowych europosłów (DimMep) wraz z mep_id
      - Dodaje losowe ustawy (DimBill) wraz z bill_id
      - Dodaje losowe głosy (FactVote)
    """
    # Pobranie nowych modeli przez apps.get_model
    MemberOfParliament = apps.get_model("main", "DimMep")
    Bill = apps.get_model("main", "DimBill")
    Vote = apps.get_model("main", "FactVote")

    fake = Faker("pl_PL")

    # 1. Tworzymy losowych "posłów" (MEP)
    numbers_counter = defaultdict(int)
    for _ in range(200):
        party = random.choice([p[0] for p in PARTIES])
        region = random.choice([r[0] for r in REGIONS])
        numbers_counter[party] += 1

        MemberOfParliament.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            party=party,
            region=region,
            number_on_list=numbers_counter[party],
            mep_id=random.randint(10000, 9999999),  # Losowy mep_id
        )

    # 2. Tworzymy losowe ustawy (DimBill)
    for _ in range(50):
        Bill.objects.create(
            bill_id=f"BILL-{uuid4().hex[:8]}",  # Poprawka: Poprawny UUID
            voting_date=fake.date_this_decade(),
            content=fake.text(),
            summary=fake.sentence(),
            title=fake.sentence(),
        )

    # Kolejne 50 ustaw bez summary:
    for _ in range(50):
        Bill.objects.create(
            bill_id=f"BILL-{uuid4().hex[:8]}",  # Poprawka: Poprawny UUID
            voting_date=fake.date_this_decade(),
            content=fake.text(),
            title=fake.sentence(),
            summary=""  # Puste summary
        )

    # 3. Dodajemy losowe głosy (FactVote)
    poslowie = list(MemberOfParliament.objects.all())
    ustawy = list(Bill.objects.all())

    for mp in poslowie:
        chosen_bills = random.sample(ustawy, min(20, len(ustawy)))

        for bill in chosen_bills:
            if not Vote.objects.filter(member_of_parliament=mp, bill=bill).exists():
                random_vote = random.choice([v[0] for v in VOTES])  # 'Z', 'P', 'W'
                Vote.objects.create(
                    member_of_parliament=mp,
                    bill=bill,
                    vote=random_vote
                )


def reverse_generate_data(apps, schema_editor):
    """
    Funkcja wykonująca się przy migracji 'reverse':
      - Usuwa dane wygenerowane w tej migracji.
    """
    MemberOfParliament = apps.get_model("main", "DimMep")
    Bill = apps.get_model("main", "DimBill")
    Vote = apps.get_model("main", "FactVote")

    Vote.objects.all().delete()
    Bill.objects.all().delete()
    MemberOfParliament.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0001_adding_super_user"),
    ]

    operations = [
        migrations.RunPython(generate_data, reverse_code=reverse_generate_data),
    ]
