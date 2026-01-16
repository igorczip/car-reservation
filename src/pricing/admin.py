# src/pricing/admin.py
"""
Admin pro pricing.

Cíl:
- vidět Quote + jeho Items na jedné stránce (Inline)
- rychlý audit cen
"""

from django.contrib import admin
from .models import PricingQuote, PricingQuoteItem


class PricingQuoteItemInline(admin.TabularInline):
    model = PricingQuoteItem
    extra = 0  # nebudeme přidávat prázdné řádky automaticky
    fields = ("code", "label", "qty", "unit_price", "amount", "locked", "created_at")
    readonly_fields = ("created_at",)


@admin.register(PricingQuote)
class PricingQuoteAdmin(admin.ModelAdmin):
    list_display = ("reservation", "status", "currency", "subtotal", "tax", "total", "priced_at_utc", "priced_by_user")
    list_filter = ("status", "currency")
    search_fields = ("reservation__human_id", "reservation__id")
    ordering = ("-created_at",)

    autocomplete_fields = ("reservation", "priced_by_user")
    inlines = [PricingQuoteItemInline]


@admin.register(PricingQuoteItem)
class PricingQuoteItemAdmin(admin.ModelAdmin):
    # Samostatná správa položek je užitečná na debug, ale obvykle stačí inline
    list_display = ("quote", "code", "label", "qty", "unit_price", "amount", "locked", "created_at")
    list_filter = ("locked", "code")
    search_fields = ("code", "label", "quote__reservation__human_id")
    ordering = ("-created_at",)

    autocomplete_fields = ("quote",)
