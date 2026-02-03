✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation
✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation

## reservations.Reservation

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `human_id` (CharField) null=False blank=True unique=True
- `owner_user` (ForeignKey) null=False blank=False unique=False
- `branch` (ForeignKey) null=False blank=False unique=False
- `vehicle` (ForeignKey) null=False blank=False unique=False
- `start_at_utc` (DateTimeField) null=False blank=False unique=False
- `end_at_utc` (DateTimeField) null=False blank=False unique=False
- `status` (CharField) null=False blank=False unique=False
- `hold_expires_at_utc` (DateTimeField) null=True blank=True unique=False
- `notes_customer` (TextField) null=False blank=True unique=False
- `notes_staff` (TextField) null=False blank=True unique=False
- `currency` (CharField) null=False blank=False unique=False
- `total_amount` (DecimalField) null=False blank=False unique=False
- `version` (PositiveIntegerField) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

## reservations.ReservationEvent

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `reservation` (ForeignKey) null=False blank=False unique=False
- `event_type` (CharField) null=False blank=False unique=False
- `actor_user` (ForeignKey) null=False blank=False unique=False
- `at_utc` (DateTimeField) null=False blank=False unique=False
- `from_status` (CharField) null=True blank=True unique=False
- `to_status` (CharField) null=True blank=True unique=False
- `delta_json` (JSONField) null=False blank=True unique=False
- `request_id` (CharField) null=False blank=True unique=False
- `ip` (CharField) null=False blank=True unique=False
- `user_agent` (CharField) null=False blank=True unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

# Code inventory: reservations

## reservations/api/serializers.py


## reservations/api/urls.py


## reservations/api/views.py

