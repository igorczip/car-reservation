✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation
✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation

## fleet.Region

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `name` (CharField) null=False blank=False unique=False
- `tz` (CharField) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

## fleet.Fleet

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `name` (CharField) null=False blank=False unique=False
- `region` (ForeignKey) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

## fleet.Branch

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `name` (CharField) null=False blank=False unique=False
- `region` (ForeignKey) null=False blank=False unique=False
- `fleet` (ForeignKey) null=False blank=False unique=False
- `tz` (CharField) null=False blank=True unique=False
- `pickup_window_min` (PositiveIntegerField) null=False blank=False unique=False
- `return_window_min` (PositiveIntegerField) null=False blank=False unique=False
- `pickup_step_min` (PositiveIntegerField) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

## fleet.Vehicle

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `branch` (ForeignKey) null=False blank=False unique=False
- `vin` (CharField) null=False blank=False unique=True
- `name` (CharField) null=False blank=False unique=False
- `status` (CharField) null=False blank=False unique=False

### Properties
- `current_plate` (property)

### Methods
- `NotUpdated()`

## fleet.VehiclePlate

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `vehicle` (ForeignKey) null=False blank=False unique=False
- `plate` (CharField) null=False blank=False unique=False
- `is_current` (BooleanField) null=False blank=False unique=False
- `valid_from` (DateTimeField) null=False blank=False unique=False
- `valid_to` (DateTimeField) null=True blank=True unique=False
- `note` (CharField) null=False blank=True unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`
- `save()` – Když ukládáme záznam jako current:

# Code inventory: fleet

## fleet/api/serializers.py


## fleet/api/urls.py


## fleet/api/views.py

