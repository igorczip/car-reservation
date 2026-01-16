# src/reservations/selectors.py
"""
Selectors = read-only dotazy.
Díky tomu je service layer čistší a testovatelnější.
"""

from django.db.models import QuerySet
from reservations.models import Reservation


def reservation_qs() -> QuerySet[Reservation]:
    """
    Základní queryset pro reservation.
    Select_related kvůli výkonu v adminu / API.
    """
    return (
        Reservation.objects
        .select_related("owner_user", "branch", "vehicle")
        .all()
    )


def get_reservation_by_id(reservation_id):
    """Bezpečné načtení rezervace (vyhazuje DoesNotExist)."""
    return reservation_qs().get(id=reservation_id)
