# src/availability/models.py
"""
AVAILABILITY doména:
- AvailabilityBlock: blokace auta na časový interval.
  Použití:
  - servis / údržba
  - ruční blokace (administrátor)
  - později i "auto je pryč" / "nepůjčovat"

Důležité:
- Start/end ukládáme do UTC (start_at_utc, end_at_utc).
- branch duplikujeme schválně, aby šly dělat rychlé dotazy "blokace pro pobočku"
  i kdyby se vehicle.branch změnilo (historicky to pak dává smysl).
"""

from django.conf import settings
from django.db import models
from common.models import UUIDModel, TimeStampedModel


class AvailabilityBlock(UUIDModel, TimeStampedModel):
    vehicle = models.ForeignKey(
        "fleet.Vehicle",
        on_delete=models.PROTECT,
        related_name="availability_blocks",
    )

    # branch držíme zvlášť pro jednodušší indexování / reporty
    branch = models.ForeignKey(
        "fleet.Branch",
        on_delete=models.PROTECT,
        related_name="availability_blocks",
    )

    start_at_utc = models.DateTimeField()
    end_at_utc = models.DateTimeField()

    reason = models.CharField(max_length=255, blank=True, default="")

    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_availability_blocks",
    )

    class Meta:
        indexes = [
            models.Index(fields=["vehicle", "start_at_utc", "end_at_utc"]),
            models.Index(fields=["branch", "start_at_utc", "end_at_utc"]),
        ]

    def __str__(self) -> str:
        return f"Block {self.vehicle_id} {self.start_at_utc}..{self.end_at_utc}"
