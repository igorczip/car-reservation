# src/reservations/services/reservation_service.py
"""
ReservationService = jediný vstupní bod pro změny rezervací.

Zásady:
- žádná doménová logika ve view ani v modelu
- všechny změny přes service
- každá změna zapíše ReservationEvent (audit)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone as dj_tz

from django.core.exceptions import ValidationError

from reservations.models import (
    Reservation,
    ReservationEvent,
    ReservationEventType,
    ReservationStatus,
)
from reservations.services.transitions import is_transition_allowed
from reservations.services.errors import (
    InvalidTransitionError,
    ConcurrencyConflictError,
)


@dataclass(frozen=True)
class RequestMeta:
    request_id: str = ""
    ip: str = ""
    user_agent: str = ""


class ReservationService:

    @staticmethod
    def _require(value, message: str):
        """
        Malý helper: pokud je hodnota falsy (None, "", 0), vyhodí ValidationError.
        V API layeru to pak mapujeme na 400.
        """
        if not value:
            raise ValidationError(message)
        return value

    @staticmethod
    def _validate_create_draft(*, owner_user, branch, vehicle, start_at_utc, end_at_utc, actor_user):
        """
        Guardy pro create_draft.
        - nechceme nechávat DB, aby nám hlásila NOT NULL
        - chceme srozumitelnou chybu pro API klienta
        """
        ReservationService._require(owner_user, "owner_user je povinný")
        ReservationService._require(actor_user, "actor_user je povinný")
        ReservationService._require(branch, "branch je povinný")
        ReservationService._require(vehicle, "vehicle je povinný")
        ReservationService._require(start_at_utc, "start_at_utc je povinný")
        ReservationService._require(end_at_utc, "end_at_utc je povinný")

        if end_at_utc <= start_at_utc:
            raise ValidationError("end_at_utc musí být > start_at_utc")

        # bezpečnost: v DB ukládáme UTC; v Django chci timezone-aware datetimes
        if dj_tz.is_naive(start_at_utc) or dj_tz.is_naive(end_at_utc):
            raise ValidationError("start_at_utc a end_at_utc musí být timezone-aware (UTC)")

        # konzistence domény: vehicle musí patřit do branch
        # (tohle je důležitý guard – jinak zrezervuješ auto z jiné pobočky)
        if getattr(vehicle, "branch_id", None) != getattr(branch, "id", None):
            raise ValidationError("vehicle nepatří do zadané branch")
    

    @staticmethod
    @transaction.atomic
    def create_draft(
        *,
       owner_user,
        branch,
        vehicle,
        start_at_utc: datetime,
        end_at_utc: datetime,
        actor_user,
       meta: RequestMeta = RequestMeta(),
    ) -> Reservation:
      
        ReservationService._validate_create_draft(
            owner_user=owner_user,
            branch=branch,
            vehicle=vehicle,
            start_at_utc=start_at_utc,
            end_at_utc=end_at_utc,
            actor_user=actor_user,
        )
        """
        Vytvoří DRAFT rezervaci.

        Poznámky:
        - zatím neřeší availability (to přijde v další kapitole)
        - zatím neřeší pricing quote (to přijde v další kapitole)
        """

        r = Reservation.objects.create(
            owner_user=owner_user,
            branch=branch,
            vehicle=vehicle,
            start_at_utc=start_at_utc,
            end_at_utc=end_at_utc,
            status=ReservationStatus.DRAFT,
            total_amount=0,
            currency="CZK",
        )

        ReservationService._log_event(
            reservation=r,
            event_type=ReservationEventType.CREATED,
            actor_user=actor_user,
            at_utc=dj_tz.now(),
            from_status=None,
            to_status=r.status,
            delta_json={
                "start_at_utc": start_at_utc.isoformat,
                "end_at_utc": end_at_utc.isoformat,
                "vehicle_id": str(vehicle.id),
                "branch_id": str(branch.id),
            },
            meta=meta,
        )

        return r

    @staticmethod
    @transaction.atomic
    def change_status(
        *,
        reservation: Reservation,
        to_status: str,
        actor_user,
        meta: RequestMeta = RequestMeta(),
        expected_version: int | None = None,
        delta_json: dict | None = None,
    ) -> Reservation:
        """
        Obecná změna statusu.
        - hlídá allowed transitions
        - hlídá optimistic locking přes `version`
        - zapisuje event

        expected_version:
        - když ho pošleš, tak service ověří, že reservation.version sedí
        """

        from_status = reservation.status

        # 1) kontrola přechodu
        if not is_transition_allowed(from_status, to_status):
            raise InvalidTransitionError(f"Nepovolený přechod {from_status} -> {to_status}")

        # 2) optimistic lock
        if expected_version is not None and reservation.version != expected_version:
            raise ConcurrencyConflictError(
                f"Verze nesedí. expected={expected_version}, actual={reservation.version}"
            )

        # 3) update + verze
        reservation.status = to_status
        reservation.version += 1
        reservation.save(update_fields=["status", "version", "updated_at"])

        # 4) event log
        ReservationService._log_event(
            reservation=reservation,
            event_type=ReservationEventType.STATUS_CHANGED,
            actor_user=actor_user,
            at_utc=dj_tz.now(),
            from_status=from_status,
            to_status=to_status,
            delta_json=delta_json or {},
            meta=meta,
        )

        return reservation

    @staticmethod
    @transaction.atomic
    def place_hold(
        *,
        reservation: Reservation,
        actor_user,
        meta: RequestMeta = RequestMeta(),
        hold_minutes: int = 15,
        expected_version: int | None = None,
    ) -> Reservation:
        """
        Přepne rezervaci do HOLD a nastaví expiration čas.
        V další kapitole sem přidáme availability check.
        """

        expires = dj_tz.now() + timedelta(minutes=hold_minutes)
        reservation.hold_expires_at_utc = expires
        reservation.save(update_fields=["hold_expires_at_utc", "updated_at"])

        return ReservationService.change_status(
            reservation=reservation,
            to_status=ReservationStatus.HOLD,
            actor_user=actor_user,
            meta=meta,
            expected_version=expected_version,
            delta_json={"hold_expires_at_utc": str(expires)},
        )

    @staticmethod
    def _log_event(
        *,
        reservation: Reservation,
        event_type: str,
        actor_user,
        at_utc,
        from_status,
        to_status,
        delta_json: dict,
        meta: RequestMeta,
    ) -> ReservationEvent:
        """
        Interní helper pro audit/event log.
        """
        return ReservationEvent.objects.create(
            reservation=reservation,
            event_type=event_type,
            actor_user=actor_user,
            at_utc=at_utc,
            from_status=from_status,
            to_status=to_status,
            delta_json=delta_json,
            request_id=meta.request_id,
            ip=meta.ip,
            user_agent=meta.user_agent,
        )
    

