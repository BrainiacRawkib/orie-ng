from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Register Contact model in the admin site."""

    list_display = ['name', 'email', 'date']
    list_filter = ['name', 'email', 'date']
    list_per_page = 50
