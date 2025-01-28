import random
from collections import defaultdict

from django.db import migrations
from faker import Faker

from main.models import PARTIES, REGIONS, VOTES


def generate_data(apps, schema_editor):
    MemberOfParliament = apps.get_model("main", "MemberOfParliament")
    Bill = apps.get_model("main", "Bill")
    Vote = apps.get_model("main", "Vote")

    fake = Faker("pl_PL")

    # -----------------------------
    # 1. Tworzymy parlamentarzystów
    # -----------------------------
    numbers_counter = defaultdict(lambda: 0)
    for _ in range(200):
        party = random.choice([p[0] for p in PARTIES])
        numbers_counter[party] += 1
        MemberOfParliament.objects.get_or_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            party=party,
            region=random.choice([r[0] for r in REGIONS]),
            number_on_list=numbers_counter[party],
        )

    # -----------------------------
    # 2. Tworzymy ustawy
    # -----------------------------
    # 50 ustaw z 'summary'
    for _ in range(50):
        Bill.objects.get_or_create(
            voting_date=fake.date_this_decade(),
            content=fake.text(),
            summary=fake.sentence(),
            title=fake.sentence(),
        )

    # +50 ustaw bez 'summary'
    for _ in range(50):
        Bill.objects.get_or_create(
            voting_date=fake.date_this_decade(),
            content=fake.text(),
            title=fake.sentence(),
        )

    # -----------------------------
    # 3. Losowe głosowania
    # -----------------------------
    poslowie = list(MemberOfParliament.objects.all())
    ustawy = list(Bill.objects.all())

    # Aby zapewnić każdemu parlamentarzyście co najmniej 20 głosów,
    # dla każdego wybieramy 20 losowych ustaw i tworzymy głosy
    # (w razie gdyby ten głos jeszcze nie istniał).
    for mp in poslowie:
        # Losujemy 20 różnych ustaw
        if len(ustawy) >= 20:
            chosen_bills = random.sample(ustawy, 20)
        else:
            # jeżeli w bazie byłoby mniej ustaw niż 20, bierzemy wszystkie
            chosen_bills = ustawy

        for bill in chosen_bills:
            if not Vote.objects.filter(member_of_parliament=mp, bill=bill).exists():
                random_vote = random.choice([v[0] for v in VOTES])  # 'Z', 'P', 'W'
                Vote.objects.create(
                    member_of_parliament=mp,
                    bill=bill,
                    vote=random_vote
                )

    # O ile chcesz jeszcze więcej głosów (ponad 20 na posła),
    # możesz dopisać dodatkową pętlę np. z 1000 losowych głosów, itd.


def reverse_generate_data(apps, schema_editor):
    MemberOfParliament = apps.get_model("main", "MemberOfParliament")
    Bill = apps.get_model("main", "Bill")
    Vote = apps.get_model("main", "Vote")

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
