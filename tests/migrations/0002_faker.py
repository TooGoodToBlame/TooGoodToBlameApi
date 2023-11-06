import random
from collections import defaultdict

from django.db import migrations
from faker import Faker

from main.models import PARTIES, REGIONS


def generate_data(apps, schema_editor):
    MemberOfParliament = apps.get_model("main", "MemberOfParliament")
    Bill = apps.get_model("main", "Bill")
    Vote = apps.get_model("main", "Vote")

    fake = Faker("pl_PL")

    numbers_counter = defaultdict(lambda: 0)
    for _ in range(200):
        party = random.choice([party[0] for party in PARTIES])
        numbers_counter[party] += 1
        MemberOfParliament.objects.get_or_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            party=party,
            region=random.choice([region[0] for region in REGIONS]),
            number_on_list=numbers_counter[party],
        )

    for _ in range(50):
        Bill.objects.get_or_create(
            voting_date=fake.date_this_decade(),
            content=fake.text(),
            summary=fake.sentence(),
            title=fake.sentence(),
        )
    for _ in range(50):
        Bill.objects.get_or_create(
            voting_date=fake.date_this_decade(),
            content=fake.text(),
            title=fake.sentence(),
        )

    poslowie = MemberOfParliament.objects.all()
    ustawy = Bill.objects.all()
    for _ in range(600):
        member_of_parliament = random.choice(poslowie)
        bill = random.choice(ustawy)
        if not Vote.objects.filter(
            member_of_parliament=member_of_parliament, bill=bill
        ).exists():
            Vote.objects.create(member_of_parliament=member_of_parliament, bill=bill)


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
