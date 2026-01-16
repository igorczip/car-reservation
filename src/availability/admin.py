# src/availability/admin.py
"""
Admin pro AvailabilityBlock.

Cíl:
- rychle najít blokace podle auta / pobočky
- vidět interval start/end (UTC)
"""

from django.contrib import admin
from .models import AvailabilityBlock


@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "branch", "start_at_utc", "end_at_utc", "reason", "created_by_user", "created_at")
    list_filter = ("branch", "vehicle", "branch__region", "branch__fleet")
    search_fields = ("vehicle__plate", "vehicle__vin", "vehicle__name", "branch__name", "reason")
    ordering = ("-start_at_utc",)

    autocomplete_fields = ("vehicle", "branch", "created_by_user")

    # Performance: přitáhne FK dopředu, admin nebude dělat N+1 dotazy
    list_select_related = ("vehicle", "branch", "created_by_user")
