from django.contrib import admin

from .models import Bill, MemberOfParliament, Vote


class MemberOfParliamentAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'party', 'region', 'number_on_list')
    search_fields = ('id','first_name', 'last_name', 'party', 'region')
    list_filter = ('party', 'region')

admin.site.register(MemberOfParliament, MemberOfParliamentAdmin)

class BillAdmin(admin.ModelAdmin):
    list_display = ('id','voting_date', 'title', 'summary', 'content')
    search_fields = ('id','title', 'voting_date')
    list_filter = ('voting_date',)

admin.site.register(Bill, BillAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('id','member_of_parliament','member_of_parliament_id', 'bill', 'vote')
    search_fields = ('id','member_of_parliament__first_name', 'member_of_parliament__last_name','member_of_parliament__id', 'bill__title')
    list_filter = ('vote', 'bill__voting_date')

admin.site.register(Vote, VoteAdmin)
