# src/reservations/admin.py
"""
Admin pro Reservation.

Slouží hlavně:
- jako target pro autocomplete_fields
- pro rychlý audit rezervací
"""

from django.contrib import admin
from .models import Reservation, ReservationEvent


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "human_id",
        "owner_user",
        "vehicle",
        "branch",
        "status",
        "start_at_utc",
        "end_at_utc",
        "created_at",
    )

    list_filter = (
        "status",
        "branch",
        "branch__region",
        "branch__fleet",
    )

    search_fields = (
        "human_id",
        "owner_user__username",
        "owner_user__email",
        "vehicle__plate",
        "vehicle__vin",
    )

    ordering = ("-created_at",)

    autocomplete_fields = (
        "owner_user",
        "vehicle",
        "branch",
    )

    list_select_related = (
        "owner_user",
        "vehicle",
        "branch",
    )


@admin.register(ReservationEvent)
class ReservationEventAdmin(admin.ModelAdmin):
    list_display = (
        "reservation",
        "event_type",
        "actor_user",
        "at_utc",
    )

    list_filter = ("event_type",)
    search_fields = ("reservation__human_id", "actor_user__username", "request_id")
    ordering = ("-at_utc",)

    autocomplete_fields = ("reservation", "actor_user")
