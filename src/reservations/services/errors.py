# src/reservations/services/errors.py
"""
Doménové chyby pro reservations service layer.
Tyto chyby budeme později mapovat na HTTP odpovědi v API.
"""


class ReservationError(Exception):
    """Base class pro všechny doménové chyby reservations."""


class InvalidTransitionError(ReservationError):
    """Pokus o nepovolený přechod stavů."""


class AvailabilityConflictError(ReservationError):
    """Rezervace koliduje s blokací nebo jinou rezervací."""


class PricingError(ReservationError):
    """Chyba při výpočtu nebo vytvoření pricing quote."""


class ConcurrencyConflictError(ReservationError):
    """Optimistic locking – někdo změnil rezervaci mezi tím."""
