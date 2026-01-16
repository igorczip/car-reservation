# src/fleet/models.py
"""
FLEET doména:
- Region: geografická/logická oblast (může mít vlastní timezone)
- Fleet: "flotila" v rámci regionu (např. firma / oddělení / skupina aut)
- Branch: pobočka (místo převzetí/vrácení), patří do Region + Fleet
- Vehicle: konkrétní auto (VIN), patří do Branch
- VehiclePlate: historie SPZ vozidla (aktuální + historické)

Poznámka:
- DB klíče jsou UUID (přes common.UUIDModel).
- created_at/updated_at máme přes common.TimeStampedModel.
- PROTECT u FK: nechceme, aby se omylem smazal region/pobočka, když na nich visí data.

Realita:
- VIN je povinný a unikátní => primární identita auta.
- SPZ se může měnit => držíme historii SPZ v samostatné tabulce.
"""

from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from common.models import UUIDModel, TimeStampedModel


class Region(UUIDModel, TimeStampedModel):
    """
    Region = oblast (např. "Praha", "Brno", "SK").
    tz = IANA timezone (Europe/Prague), slouží pro výpočty lokálních časů,
    ale do DB ukládáme časy vždy v UTC.
    """
    name = models.CharField(max_length=120)
    tz = models.CharField(max_length=64, default="UTC")

    def __str__(self) -> str:
        return self.name


class Fleet(UUIDModel, TimeStampedModel):
    """
    Fleet = flotila vozidel v rámci regionu (logická skupina).
    """
    name = models.CharField(max_length=120)

    # PROTECT: pokud existuje fleet, region nesmí zmizet pod nohama
    region = models.ForeignKey(
        "fleet.Region",
        on_delete=models.PROTECT,
        related_name="fleets",
    )

    def __str__(self) -> str:
        return self.name


class Branch(UUIDModel, TimeStampedModel):
    """
    Branch = pobočka, kde probíhá pickup/return.
    Zde dává smysl mít parametry pro pravidla (časové okno, krok atd.)
    - tz může být prázdné => použijeme region.tz (logika později ve službách).
    """
    name = models.CharField(max_length=120)

    region = models.ForeignKey(
        "fleet.Region",
        on_delete=models.PROTECT,
        related_name="branches",
    )
    fleet = models.ForeignKey(
        "fleet.Fleet",
        on_delete=models.PROTECT,
        related_name="branches",
    )

    # Pokud je prázdné, počítá se tz z Region.tz
    tz = models.CharField(max_length=64, blank=True, default="")

    # "window" = toleranční okno kolem času
    pickup_window_min = models.PositiveIntegerField(default=30)
    return_window_min = models.PositiveIntegerField(default=30)

    # "step" = krok výběru času (např. po 15 min)
    pickup_step_min = models.PositiveIntegerField(default=15)

    def __str__(self) -> str:
        return self.name


class VehicleStatus(models.TextChoices):
    """
    Stav vozidla.
    Pozn.: toto NENÍ stav rezervace, jen dostupnost auta.
    """
    ACTIVE = "ACTIVE", "ACTIVE"
    MAINTENANCE = "MAINTENANCE", "MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE", "OUT_OF_SERVICE"


class Vehicle(UUIDModel, TimeStampedModel):
    """
    Vehicle = konkrétní auto.
    - VIN je povinný a unique => primární identita.
    - SPZ řešíme přes VehiclePlate (historie), protože SPZ se může měnit.
    - branch říká "kde je auto doma" (primární pobočka).
    """
    branch = models.ForeignKey(
        "fleet.Branch",
        on_delete=models.PROTECT,
        related_name="vehicles",
    )

    vin = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)

    status = models.CharField(
        max_length=32,
        choices=VehicleStatus.choices,
        default=VehicleStatus.ACTIVE,
    )

    class Meta:
        # Indexy pomůžou pro filtrování v UI i API (např. "všechna active auta na pobočce")
        indexes = [
            models.Index(fields=["branch", "status"]),
        ]

    @property
    def current_plate(self) -> str | None:
        """
        Vrátí aktuální SPZ vozidla.

        Logika:
        1) Pokud je k dispozici prefetchnutá current SPZ (typicky z Django admin listu),
           použije ji bez dalšího DB dotazu.
        2) Pokud prefetched data nejsou k dispozici (např. v API, shellu, službě),
           provede standardní dotaz do DB.

        Výsledek:
        - V admin listu: žádné N+1 dotazy
        - Mimo admin: bezpečné a čitelné chování
        """
        # 1) Optimalizovaná cesta – admin list s prefetch_related
        prefetched = getattr(self, "_prefetched_current_plates", None)
        if prefetched is not None:
            return prefetched[0].plate if prefetched else None

        # 2) Fallback – běžný dotaz (např. API, shell, služby)
        current = self.plates.filter(is_current=True).only("plate").first()
        return current.plate if current else None

    def __str__(self) -> str:
        plate = self.current_plate or "bez SPZ"
        return f"{self.name} ({plate})"


class VehiclePlate(UUIDModel, TimeStampedModel):
    """
    Historie SPZ vozidla.

    Pravidla:
    1) Jedno vozidlo může mít pouze 1 aktuální SPZ (is_current=True).
    2) Jedna SPZ může být aktuální pouze u 1 vozidla (globálně).
    3) Historie se může opakovat (tj. plate v minulosti může existovat vícekrát).

    valid_from/valid_to:
    - current záznam má typicky valid_to = NULL
    - při přidání nové current SPZ automaticky "uzavřeme" předchozí current (valid_to)
    """
    vehicle = models.ForeignKey(
        "fleet.Vehicle",
        on_delete=models.CASCADE,
        related_name="plates",
    )

    plate = models.CharField(max_length=32)
    is_current = models.BooleanField(default=True)

    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(blank=True, null=True)

    note = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        constraints = [
            # Jedna aktuální SPZ globálně (pouze pro is_current=True)
            models.UniqueConstraint(
                fields=["plate"],
                condition=Q(is_current=True),
                name="uniq_current_plate_global",
            ),
            # Jedna aktuální SPZ na jedno vozidlo (pouze pro is_current=True)
            models.UniqueConstraint(
                fields=["vehicle"],
                condition=Q(is_current=True),
                name="uniq_current_plate_per_vehicle",
            ),
        ]
        indexes = [
            models.Index(fields=["plate"]),
            models.Index(fields=["vehicle", "is_current"]),
        ]

    def save(self, *args, **kwargs):
        """
        Když ukládáme záznam jako current:
        - uzavřeme předchozí current SPZ u stejného vozidla
        - nastavíme valid_to = NULL (protože je aktuální)
        """
        with transaction.atomic():
            if self.is_current:
                now = timezone.now()

                # Zamkneme řádky current SPZ pro vozidlo (aby nevznikl race condition)
                qs = VehiclePlate.objects.select_for_update().filter(
                    vehicle=self.vehicle,
                    is_current=True,
                )

                # pokud editujeme existující záznam, vynecháme sebe
                if self.pk:
                    qs = qs.exclude(pk=self.pk)

                # uzavřeme předchozí current
                qs.update(is_current=False, valid_to=now)

                # current záznam nemá valid_to
                self.valid_to = None

                # pokud někdo poslal prázdný valid_from, nastavíme ho
                if not self.valid_from:
                    self.valid_from = now

            super().save(*args, **kwargs)

    def __str__(self) -> str:
        suffix = " (current)" if self.is_current else ""
        return f"{self.plate}{suffix}"
