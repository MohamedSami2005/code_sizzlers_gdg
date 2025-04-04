from django.contrib import admin
from .models import UzhavanHub

@admin.register(UzhavanHub)
class UzhavanHubAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'manager', 'contact_number')
    search_fields = ('name', 'location')
    list_filter = ('manager',)
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'manager')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'operational_hours')
        }),
        ('Geolocation', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    )