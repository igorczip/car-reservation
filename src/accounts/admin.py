# src/accounts/admin.py
"""
Admin pro profily uživatelů.

Poznámka:
- Django User je standardní model; profily jsou vedle něj.
- Pro MVP budeme spravovat profily zvlášť.
"""

from django.contrib import admin
from .models import CustomerProfile, StaffProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "phone", "user", "created_at")
    search_fields = ("email", "full_name", "phone", "user__username", "user__email")
    ordering = ("-created_at",)

    autocomplete_fields = ("user",)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "scope_type", "scope_branch", "scope_fleet", "scope_region", "created_at")
    list_filter = ("scope_type",)
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)

    autocomplete_fields = ("user", "scope_branch", "scope_fleet", "scope_region")

    # Tip: později dáme validaci, že je vyplněný přesně jeden scope_* dle scope_type.
