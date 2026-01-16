# src/accounts/models.py
"""
ACCOUNTS doména:
- CustomerProfile: rozšíření pro běžného zákazníka (kdo si rezervuje auto)
- StaffProfile: rozšíření pro zaměstnance (operátor pobočky/fleetu/regionu)

Proč profil?
- Django User je obecný; profil drží doménová data (phone, scope, ...)

Scope u staff:
- staff může mít oprávnění jen pro BRANCH nebo FLEET nebo REGION
- v DB to modelujeme přes scope_type + 3 volitelné FK
- validaci "vyplněný přesně jeden scope_..." uděláme později ve service layer
"""

from django.conf import settings
from django.db import models
from common.models import UUIDModel, TimeStampedModel


class CustomerProfile(UUIDModel, TimeStampedModel):
    """
    CustomerProfile = data k zákazníkovi.
    user = vazba na Django auth user.
    email držíme i tady (pragmaticky) - později můžeme synchronizovat.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )

    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True, default="")
    full_name = models.CharField(max_length=160, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        return self.full_name or self.email


class StaffScopeType(models.TextChoices):
    """
    Jak široký je scope zaměstnance:
    - BRANCH: vidí jen pobočku
    - FLEET: vidí flotilu
    - REGION: vidí region
    """
    BRANCH = "BRANCH", "BRANCH"
    FLEET = "FLEET", "FLEET"
    REGION = "REGION", "REGION"


class StaffProfile(UUIDModel, TimeStampedModel):
    """
    StaffProfile = profil zaměstnance.
    scope_type říká, který FK z trio (branch/fleet/region) je relevantní.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )

    scope_type = models.CharField(max_length=16, choices=StaffScopeType.choices)

    # Jen jeden z těchto scope_* má být vyplněn - dle scope_type
    scope_branch = models.ForeignKey("fleet.Branch", null=True, blank=True, on_delete=models.PROTECT)
    scope_fleet = models.ForeignKey("fleet.Fleet", null=True, blank=True, on_delete=models.PROTECT)
    scope_region = models.ForeignKey("fleet.Region", null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"Staff({self.user_id}) {self.scope_type}"
