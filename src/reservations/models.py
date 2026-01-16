# src/reservations/models.py
from django.conf import settings
from django.db import models

# Pozn.: UniqueConstraint je importnutý, ale v tomto MVP skeletonu zatím není použitý.
# Může to být pozůstatek pro budoucí rozšíření (např. idempotence, request_id unikátnost apod.)
from django.db.models import UniqueConstraint  # noqa: F401

from common.models import UUIDModel, TimeStampedModel


class ReservationStatus(models.TextChoices):
    """
    Stav rezervace (state machine).
    V MVP zatím jen enum + status field; skutečné přechody a guardy budou v service layer.
    """

    DRAFT = "DRAFT", "DRAFT"           # koncept / rozpracované
    HOLD = "HOLD", "HOLD"              # dočasná blokace (typicky časově omezená)
    CONFIRMED = "CONFIRMED", "CONFIRMED"
    PICKED_UP = "PICKED_UP", "PICKED_UP"
    RETURNED = "RETURNED", "RETURNED"
    CANCELED = "CANCELED", "CANCELED"
    EXPIRED = "EXPIRED", "EXPIRED"     # např. hold vypršel a rezervace se ukončila


class Reservation(UUIDModel, TimeStampedModel):
    """
    Rezervace vozidla v čase.
    Všechny časy držíme v UTC (stejný důvod jako u AvailabilityBlock).
    """

    # "human friendly" identifikátor:
    # - unikátní
    # - pro MVP může zůstat prázdné (generování doplní service layer)
    human_id = models.CharField(max_length=32, unique=True, blank=True, default="")

    # Kdo rezervaci vlastní (zákazník). PROTECT kvůli historii rezervací.
    owner_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservations")

    # Pobočka a vozidlo, kterého se rezervace týká
    branch = models.ForeignKey("fleet.Branch", on_delete=models.PROTECT, related_name="reservations")
    vehicle = models.ForeignKey("fleet.Vehicle", on_delete=models.PROTECT, related_name="reservations")

    # Interval rezervace v UTC
    start_at_utc = models.DateTimeField()
    end_at_utc = models.DateTimeField()

    # Stav rezervace – default DRAFT
    status = models.CharField(max_length=16, choices=ReservationStatus.choices, default=ReservationStatus.DRAFT)

    # Pokud je rezervace v HOLD, tady držíme deadline vypršení hold.
    # null/blank: pro stavy mimo HOLD nevyplněno.
    hold_expires_at_utc = models.DateTimeField(null=True, blank=True)

    # Poznámky:
    # - notes_customer: viditelné pro zákazníka (nebo od zákazníka)
    # - notes_staff: interní poznámky (přístup staff only)
    notes_customer = models.TextField(blank=True, default="")
    notes_staff = models.TextField(blank=True, default="")

    # Pricing základ:
    # currency: měna rezervace (MVP default CZK)
    # total_amount: celková cena (v MVP default 0; přepočty dělá pricing modul)
    currency = models.CharField(max_length=8, default="CZK")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Optimistic concurrency control:
    # - při update service layer zvýší version o 1
    # - při konkurentním update lze detekovat konflikt (pokud nesedí očekávaná version)
    version = models.PositiveIntegerField(default=0)

    class Meta:
        # Indexy pro konfliktní vyhledávání a listování:
        # - intervalové dotazy (vehicle/branch + start/end)
        # - filtrace podle statusu (např. "aktivní rezervace")
        indexes = [
            models.Index(fields=["vehicle", "start_at_utc", "end_at_utc"]),
            models.Index(fields=["branch", "start_at_utc", "end_at_utc"]),
            models.Index(fields=["status"]),
        ]

        # Pozn.: sem později často patří constraints typu:
        # - end_at_utc > start_at_utc (CheckConstraint)
        # - vehicle musí patřit do branch (enforce ve service layer nebo constraintem)
        # Zatím necháváme MVP skeleton.

    def __str__(self) -> str:
        # Pokud máme human_id, je to nejlepší pro admin/logy,
        # jinak fallback na UUID
        return self.human_id or str(self.id)


class ReservationEventType(models.TextChoices):
    """
    Typ eventu v event-sourcing stylu logu.
    Eventy slouží pro:
    - audit (kdo co změnil)
    - debug produkčních incidentů
    - případné "replay" nebo rekonstrukci historie
    """

    CREATED = "CREATED", "CREATED"
    UPDATED = "UPDATED", "UPDATED"
    STATUS_CHANGED = "STATUS_CHANGED", "STATUS_CHANGED"

    HOLD_PLACED = "HOLD_PLACED", "HOLD_PLACED"
    HOLD_RESET = "HOLD_RESET", "HOLD_RESET"
    HOLD_EXPIRED = "HOLD_EXPIRED", "HOLD_EXPIRED"

    CONFIRMED = "CONFIRMED", "CONFIRMED"
    PICKED_UP = "PICKED_UP", "PICKED_UP"
    RETURNED = "RETURNED", "RETURNED"
    CANCELED = "CANCELED", "CANCELED"

    VEHICLE_CHANGED = "VEHICLE_CHANGED", "VEHICLE_CHANGED"
    TIME_CHANGED = "TIME_CHANGED", "TIME_CHANGED"
    PRICE_CHANGED = "PRICE_CHANGED", "PRICE_CHANGED"
    BRANCH_CHANGED = "BRANCH_CHANGED", "BRANCH_CHANGED"

    CONFLICT_DETECTED = "CONFLICT_DETECTED", "CONFLICT_DETECTED"
    IDP_REPLAYED = "IDP_REPLAYED", "IDP_REPLAYED"


class ReservationEvent(UUIDModel, TimeStampedModel):
    """
    Auditní/event log pro Reservation.

    Důležité:
    - reservation: CASCADE, protože eventy bez parent rezervace nedávají smysl
    - actor_user: PROTECT, protože chceme zachovat audit stopu i po změnách uživatelů
    """

    reservation = models.ForeignKey("reservations.Reservation", on_delete=models.CASCADE, related_name="events")

    # Typ eventu z enumu
    event_type = models.CharField(max_length=32, choices=ReservationEventType.choices)

    # Kdo event způsobil (uživatel, staff, systémový uživatel atd.)
    actor_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservation_events")

    # Čas eventu v UTC
    at_utc = models.DateTimeField()

    # Pokud event mění status, uložíme odkud/kam (pro audit i pro analýzu)
    from_status = models.CharField(max_length=16, choices=ReservationStatus.choices, null=True, blank=True)
    to_status = models.CharField(max_length=16, choices=ReservationStatus.choices, null=True, blank=True)

    # Delta změn jako JSON:
    # - default=dict: každá instance dostane vlastní dict (bez sdílené mutable default chyby)
    # - blank=True: admin dovolí prázdné
    delta_json = models.JSONField(default=dict, blank=True)

    # Idempotence / observabilita:
    # request_id: pro korelaci v logách (např. X-Request-ID z API gateway)
    # ip, user_agent: základní forenzní data (volitelné)
    request_id = models.CharField(max_length=128, blank=True, default="")
    ip = models.CharField(max_length=64, blank=True, default="")
    user_agent = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        # Indexy pro:
        # - rychlé načtení timeline eventů rezervace (reservation + at)
        # - filtrování podle event_type
        # - dohledání eventů podle request_id (debug)
        indexes = [
            models.Index(fields=["reservation", "at_utc"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["request_id"]),
        ]

        # Později se často doplňuje constraint typu:
        # UniqueConstraint(fields=["request_id", "event_type"], ...) pro idempotenci,
        # ale jen pokud request_id zaručeně existuje a má smysl to enforceovat v DB.

    def __str__(self) -> str:
        return f"{self.event_type} {self.reservation_id}"
