from django.contrib import admin

from .models import Bill, MemberOfParliament, Vote

admin.site.register(MemberOfParliament)
admin.site.register(Bill)
admin.site.register(Vote)
