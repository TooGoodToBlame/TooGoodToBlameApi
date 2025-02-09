from django.contrib import admin

# Importuj nowe modele:
from .models import DimMep, DimBill, FactVote

@admin.register(DimMep)
class DimMepAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'party', 'region', 'number_on_list')
    search_fields = ('id', 'first_name', 'last_name', 'party', 'region')
    list_filter = ('party', 'region')


@admin.register(DimBill)
class DimBillAdmin(admin.ModelAdmin):
    list_display = ('id', 'voting_date', 'title', 'summary', 'content')
    search_fields = ('id', 'title', 'voting_date', 'content')
    list_filter = ('voting_date',)


@admin.register(FactVote)
class FactVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_of_parliament', 'member_of_parliament_id', 'bill', 'vote')
    search_fields = (
        'id',
        'member_of_parliament__first_name', 
        'member_of_parliament__last_name', 
        'member_of_parliament__id',
        'bill__title'
    )
    list_filter = ('vote', 'bill__voting_date')
