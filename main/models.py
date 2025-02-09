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
    ("W", "Wstrzymany"),
)


class DimCountry(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    mep_count = models.SmallIntegerField(null=True, blank=True)
    valid_from = models.DateField(auto_now_add=True)
    valid_to = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.name or "Unknown Country"

class DimPoliticalGroup(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    ideology = models.CharField(max_length=200, null=True, blank=True)
    foundation_date = models.DateField(null=True, blank=True)
    valid_from = models.DateField(auto_now_add=True)
    valid_to = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.name or "Unknown Political Group"

class DimTime(models.Model):
    day = models.CharField(max_length=20, null=True, blank=True)
    month = models.CharField(max_length=20, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    time_of_the_day = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time_strings = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.time_strings or "Unknown Time"


class DimSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.session_id

class DimMep(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    party = models.CharField(max_length=50, choices=PARTIES)
    region = models.CharField(max_length=50, choices=REGIONS)
    number_on_list = models.SmallIntegerField(null=True, blank=True)

    mep_id = models.IntegerField()
    parlimentary_term = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    valid_from = models.DateField(auto_now_add=True)
    valid_to = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DimBill(models.Model):
    dim_amendmend = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    dim_session = models.ForeignKey(DimSession, on_delete=models.SET_NULL, null=True, blank=True)
    bill_id = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=False)
    bill_type = models.IntegerField(null=True, blank=True)
    decision = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    active_since = models.DateField(null=True, blank=True)
    active_till = models.DateField(null=True, blank=True)
    valid_from = models.DateField(auto_now_add=True)
    voting_date = models.DateField()
    summary = models.TextField(null=True, blank=False)
    title = models.CharField(max_length=50)
    result = models.CharField(
        max_length=3,
        choices=VOTES,
        default="P",
    )

    def __str__(self):
        return f"{self.voting_date} - {self.title}"


class FactVote(models.Model):
    member_of_parliament = models.ForeignKey(
        DimMep, on_delete=models.CASCADE, related_name="votes"
    )
    bill = models.ForeignKey(
        DimBill, on_delete=models.CASCADE, related_name="votes"
    )

    dim_time = models.ForeignKey(DimTime, on_delete=models.CASCADE, null=True, blank=True)
    dim_session = models.ForeignKey(DimSession, on_delete=models.CASCADE, null=True, blank=True)

    vote = models.CharField(max_length=1, choices=VOTES)

    class Meta:
        unique_together = ["member_of_parliament", "bill"]

    def __str__(self):
        return f"Głos posła {self.member_of_parliament} na ustawę {self.bill}"


class FactAttendance(models.Model):
    dim_mep = models.ForeignKey(DimMep, on_delete=models.CASCADE)
    dim_session = models.ForeignKey(DimSession, on_delete=models.CASCADE)
    dim_time = models.ForeignKey(DimTime, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attendance({self.dim_mep}, {self.dim_session}, {self.dim_time})"
