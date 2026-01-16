# src/reservations/services/transitions.py
"""
Přechody stavů rezervace (state machine).

Poznámka:
- Model obsahuje jen enum + field.
- Veškerá pravidla přechodů jsou tady (service layer).
"""

from reservations.models import ReservationStatus

# Povolené přechody: (from_status) -> {to_status1, to_status2, ...}
ALLOWED_TRANSITIONS = {
    ReservationStatus.DRAFT: {
        ReservationStatus.HOLD,
        ReservationStatus.CANCELED,
    },
    ReservationStatus.HOLD: {
        ReservationStatus.CONFIRMED,
        ReservationStatus.CANCELED,
        ReservationStatus.EXPIRED,
    },
    ReservationStatus.CONFIRMED: {
        ReservationStatus.PICKED_UP,
        ReservationStatus.CANCELED,
    },
    ReservationStatus.PICKED_UP: {
        ReservationStatus.RETURNED,
    },
    ReservationStatus.RETURNED: set(),
    ReservationStatus.CANCELED: set(),
    ReservationStatus.EXPIRED: set(),
}


def is_transition_allowed(from_status: str, to_status: str) -> bool:
    """Vrátí True, pokud je přechod povolený."""
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set())
