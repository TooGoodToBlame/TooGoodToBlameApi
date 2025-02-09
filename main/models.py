from django.db import models

PARTIES = (
    ("EPP", "European People's Party"),
    ("S&D", "Progressive Alliance of Socialists and Democrats"),
    ("PfE", "Patriots for Europe"),
    ("ECR", "European Conservatives and Reformists"),
    ("Renew Europe", "Renew Europe"),
    ("Greens/EFA", "The Greens/European Free Alliance"),
    ("The Left", "The Left in the European Parliament - GUE/NGL"),
    ("ESN", "Europe of Sovereign Nations"),
)

REGIONS = (
    ("DS", "Dolnośląskie"),
    ("KP", "Kujawsko-Pomorskie"),
    ("LB", "Lubuskie"),
    ("LD", "Łódzkie"),
    ("LU", "Lubelskie"),
    ("MA", "Małopolskie"),
    ("MZ", "Mazowieckie"),
    ("OP", "Opolskie"),
    ("PK", "Podkarpackie"),
    ("PD", "Podlaskie"),
    ("PM", "Pomorskie"),
    ("SL", "Śląskie"),
    ("SW", "Świętokrzyskie"),
    ("WN", "Warmińsko-Mazurskie"),
    ("WP", "Wielkopolskie"),
    ("ZP", "Zachodniopomorskie"),
)


VOTES = (
    ("Z", "Za"),
    ("P", "Przeciw"),
    ("W", "Wstzymany"),
)


class MemberOfParliament(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    party = models.CharField(max_length=50, choices=PARTIES)
    region = models.CharField(max_length=50, choices=REGIONS)
    number_on_list = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Bill(models.Model):
    voting_date = models.DateField()
    content = models.TextField(null=True, blank=False)
    summary = models.TextField(null=True, blank=False)
    title = models.CharField(max_length=50)
    result = models.CharField(
        max_length=3,
        choices=VOTES,
        default="P",
    )

    def __str__(self):
        return f"{self.voting_date} - {self.title}"


class Vote(models.Model):
    member_of_parliament = models.ForeignKey(
        MemberOfParliament, on_delete=models.CASCADE
    )
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    vote = models.CharField(max_length=1, choices=VOTES)

    class Meta:
        unique_together = ["member_of_parliament", "bill"]

    def __str__(self):
        return f"Głos posła {self.member_of_parliament} na ustawę {self.bill}"
