✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation
✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation

## availability.AvailabilityBlock

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `vehicle` (ForeignKey) null=False blank=False unique=False
- `branch` (ForeignKey) null=False blank=False unique=False
- `start_at_utc` (DateTimeField) null=False blank=False unique=False
- `end_at_utc` (DateTimeField) null=False blank=False unique=False
- `reason` (CharField) null=False blank=True unique=False
- `created_by_user` (ForeignKey) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

# Code inventory: availability

## availability/api/serializers.py


## availability/api/urls.py


## availability/api/views.py

