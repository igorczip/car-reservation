# src/fleet/admin.py
"""
Django Admin konfigurace pro FLEET.

Cíl:
- mít rychlé listy (columns, filtry, search)
- mít přehledné editace (fieldsets)
- mít rychlé prokliky (autocomplete_fields, raw_id_fields)
"""

from django.contrib import admin
from django.db.models import Prefetch
from .models import Region, Fleet, Branch, Vehicle, VehiclePlate


class VehiclePlateInline(admin.TabularInline):
    """
    Inline historie SPZ u vozidla:
    - umožní ruční přidání nové SPZ
    - uvidíš historii včetně valid_from/valid_to
    """
    model = VehiclePlate
    extra = 0
    fields = ("plate", "is_current", "valid_from", "valid_to", "note", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-valid_from",)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    # co se zobrazí ve výpisu
    list_display = ("name", "tz", "created_at", "updated_at")
    # filtry vpravo
    list_filter = ("tz",)
    # hledání nahoře
    search_fields = ("name", "tz")
    # řazení
    ordering = ("name",)


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "created_at", "updated_at")
    list_filter = ("region",)
    search_fields = ("name", "region__name")
    ordering = ("region__name", "name")

    # u větších DB je lepší autocomplete než dropdown
    autocomplete_fields = ("region",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "region",
        "fleet",
        "tz",
        "pickup_window_min",
        "return_window_min",
        "pickup_step_min",
        "created_at",
    )
    list_filter = ("region", "fleet")
    search_fields = ("name", "region__name", "fleet__name")
    ordering = ("region__name", "fleet__name", "name")

    autocomplete_fields = ("region", "fleet")

    # Přehlednější layout formuláře
    fieldsets = (
        ("Základ", {"fields": ("name", "region", "fleet")}),
        ("Timezone", {"fields": ("tz",)}),
        ("Pickup/Return pravidla", {"fields": ("pickup_window_min", "return_window_min", "pickup_step_min")}),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("name", "current_plate", "vin", "branch", "status", "created_at")
    list_filter = ("status", "branch", "branch__region", "branch__fleet")

    # POZOR: current_plate je property => admin search přes SQL to neumí
    # Hledáme přes historii SPZ (VehiclePlate) pomocí related_name="plates"
    search_fields = ("name", "vin", "branch__name", "plates__plate")

    ordering = ("branch__name", "name")
    autocomplete_fields = ("branch",)

    # Užitečné v adminu: rychlý přechod na edit
    list_select_related = ("branch",)

    inlines = (VehiclePlateInline,)

    def get_search_results(self, request, queryset, search_term):
        """
        Protože search_fields obsahuje join na plates__plate,
        může queryset vracet duplicitní Vehicle řádky.
        Nastavíme distinct().
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, True

    def get_queryset(self, request):
        """
        Optimalizace: current_plate je property a jinak by dělala N+1 dotazů.
        Prefetchneme jen aktuální SPZ (is_current=True) pro všechna auta ve výpisu.
        """
        qs = super().get_queryset(request)

        current_plates_qs = VehiclePlate.objects.filter(is_current=True).only(
            "id", "vehicle_id", "plate", "is_current"
        )

        return qs.prefetch_related(
            Prefetch("plates", queryset=current_plates_qs, to_attr="_prefetched_current_plates")
        )



