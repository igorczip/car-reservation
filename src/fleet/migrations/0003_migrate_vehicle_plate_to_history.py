from django.db import migrations
from django.utils import timezone


def forwards(apps, schema_editor):
    Vehicle = apps.get_model("fleet", "Vehicle")
    VehiclePlate = apps.get_model("fleet", "VehiclePlate")

    now = timezone.now()

    # V tomto kroku Vehicle pořád obsahuje sloupec 'plate' v DB
    for v in Vehicle.objects.exclude(plate__isnull=True).exclude(plate=""):
        VehiclePlate.objects.get_or_create(
            vehicle_id=v.id,
            plate=v.plate,
            defaults={
                "is_current": True,
                "valid_from": now,
                "valid_to": None,
                "note": "Migrace z původního Vehicle.plate",
            },
        )


def backwards(apps, schema_editor):
    # Volitelně: smazat záznamy vytvořené migrací.
    # Nechávám jako noop, protože rollback dat je u historie většinou nežádoucí.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("fleet", "0002_remove_vehicle_plate_vehicleplate"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
