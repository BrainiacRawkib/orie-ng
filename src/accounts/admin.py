from django.contrib import admin
from .models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_customer', 'is_merchant', 'is_mvp', 'email', 'contact']
    list_filter = ['is_customer', 'is_merchant']
    list_display_links = ['id', 'username']
    list_editable = ['is_customer', 'is_merchant', 'is_mvp']
    list_per_page = 20


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id', 'user']
    raw_id_fields = ['user']
    list_per_page = 20
