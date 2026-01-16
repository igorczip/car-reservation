# Car Reservation – Fleet Domain

Tento projekt je backendová část systému pro správu vozového parku a rezervací vozidel.
Backend je postavený na **Django + PostgreSQL** a je navržen s důrazem na:
- reálný datový model (VIN, SPZ, historie),
- konzistenci dat na úrovni databáze,
- čitelnou a bezpečnou správu přes Django Admin.

---

## 🧩 Fleet doména – přehled

Fleet doména reprezentuje **strukturu vozového parku** a jeho geografické/logické členění.

### Entity:
- **Region** – geografická nebo logická oblast (timezone)
- **Fleet** – flotila vozidel v rámci regionu
- **Branch** – pobočka (pickup / return)
- **Vehicle** – konkrétní vozidlo (identifikované VIN)
- **VehiclePlate** – historie registračních značek (SPZ)

---

## 🚗 Vehicle – klíčové rozhodnutí v návrhu

### VIN jako primární identita
- `VIN` je **povinný a unikátní**
- slouží jako **primární identifikátor vozidla**
- VIN se **nikdy nemění**

```python
vin = models.CharField(max_length=32, unique=True)


SPZ (plate) jako historizovaný atribut
V reálném světě:
SPZ se může měnit (přepis, výměna, dočasná značka),
ale vozidlo (VIN) zůstává stejné.
➡️ Proto SPZ není uložená přímo ve Vehicle, ale v samostatné tabulce VehiclePlate.

🧾 VehiclePlate – historie SPZ
Základní vlastnosti:
jedna SPZ = jeden záznam v historii
SPZ může existovat historicky vícekrát
aktuální SPZ (is_current=True) je vždy jen jedna

class VehiclePlate(UUIDModel, TimeStampedModel):
    vehicle = models.ForeignKey("fleet.Vehicle", ...)
    plate = models.CharField(max_length=32)
    is_current = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(null=True, blank=True)

Databázová pravidla (DB constraints)

Databáze garantuje konzistenci:
UNIQUE (plate) WHERE is_current = true

Jedna aktuální SPZ na jedno vozidlo
UNIQUE (vehicle_id) WHERE is_current = true

🔄 Automatická správa historie SPZ
Při uložení nové SPZ jako is_current=True:
předchozí current SPZ se automaticky uzavře (valid_to)
nový záznam se stane jediným aktuálním
Tato logika je implementována přímo v modelu VehiclePlate.save() a běží v databázové transakci.

Django Admin
Admin rozhraní je navrženo pro ruční správu vozového parku.

Vehicle admin:
    zobrazuje aktuální SPZ (current_plate)
    umožňuje vyhledávání i podle historických SPZ
    optimalizovaný proti N+1 dotazům

Inline historie SPZ:
    VehiclePlate je spravována inline u Vehicle
    změna SPZ nevyžaduje ruční editaci starých záznamů

🚀 Optimalizace výkonu
Property Vehicle.current_plate:
    využívá prefetch_related v admin listu
    fallbackuje na standardní dotaz mimo admin
    je bezpečná pro použití v API, službách i shellu

🗄️ Migrace
Přechod z původního modelu (Vehicle.plate) proběhl v několika krocích:
    vytvoření tabulky VehiclePlate
    migrace existujících SPZ do historie
    odstranění sloupce plate z Vehicle
Migrace jsou idempotentní a zachovávají všechna existující data.

✅ Stav projektu
    VIN jako primární identita
    Historie SPZ
    DB-level ochrana proti konfliktům
    Admin připravený pro reálné použití
    Optimalizace dotazů

🛠️ Technologie
        Python 3.12
        Django
        PostgreSQL
        Docker / Docker Compose
        Poetry
