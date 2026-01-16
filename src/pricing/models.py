# src/pricing/models.py
"""
PRICING doména:
- PricingQuote: cenová kalkulace k rezervaci (může být více verzí, typicky Draft/Final)
- PricingQuoteItem: položky quote (např. base rental, insurance, discount, fee)

Proč Quote?
- Cena se může měnit podle pravidel; quote umožní:
  - přepočty
  - audit, co bylo účtováno
  - "zamknutí" položek (locked), když má být final
"""

from django.conf import settings
from django.db import models
from common.models import UUIDModel, TimeStampedModel


class QuoteStatus(models.TextChoices):
    DRAFT = "DRAFT", "DRAFT"
    FINAL = "FINAL", "FINAL"


class PricingQuote(UUIDModel, TimeStampedModel):
    # Napojení na rezervaci
    reservation = models.ForeignKey(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="quotes",
    )

    status = models.CharField(max_length=16, choices=QuoteStatus.choices, default=QuoteStatus.DRAFT)

    currency = models.CharField(max_length=8, default="CZK")

    # Součty držíme explicitně (lepší pro výkon a audit)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # kdo a kdy quote spočítal/uzavřel
    priced_at_utc = models.DateTimeField(null=True, blank=True)
    priced_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="priced_quotes",
    )

    class Meta:
        indexes = [
            models.Index(fields=["reservation", "status"]),
        ]

    def __str__(self) -> str:
        return f"Quote {self.reservation_id} {self.status}"


class PricingQuoteItem(UUIDModel, TimeStampedModel):
    quote = models.ForeignKey(
        "pricing.PricingQuote",
        on_delete=models.CASCADE,
        related_name="items",
    )

    # code = strojový identifikátor položky (např. "BASE_RENTAL", "INSURANCE_BASIC")
    code = models.CharField(max_length=64)

    # label = text do UI / faktury
    label = models.CharField(max_length=160)

    # qty a unit_price jako Decimal (peníze + přesnost)
    qty = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # amount můžeš buď dopočítat ve service layer, nebo držet uložené (audit)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # locked = položka už se nesmí měnit (quote FINAL)
    locked = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["quote", "code"]),
        ]

    def __str__(self) -> str:
        return f"{self.code} {self.amount}"
