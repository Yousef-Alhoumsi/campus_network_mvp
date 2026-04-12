from django.contrib import admin
from .models import Profile, Opportunity, Event


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = ['title', 'organization', 'location', 'is_paid']

    list_filter = ("is_paid", "location")

    search_fields = ("title", "organization", "description")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location')
    list_filter = ('date_time',)
    search_fields = ('title', 'location')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "major")
    search_fields = ('user__username', 'user__first_name', 'user__email', "major")




