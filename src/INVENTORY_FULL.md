✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation
✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation

## accounts.CustomerProfile

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `user` (OneToOneField) null=False blank=False unique=True
- `email` (EmailField) null=False blank=False unique=False
- `phone` (CharField) null=False blank=True unique=False
- `full_name` (CharField) null=False blank=True unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

## accounts.StaffProfile

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `user` (OneToOneField) null=False blank=False unique=True
- `scope_type` (CharField) null=False blank=False unique=False
- `scope_branch` (ForeignKey) null=True blank=True unique=False
- `scope_fleet` (ForeignKey) null=True blank=True unique=False
- `scope_region` (ForeignKey) null=True blank=True unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

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

## pricing.PricingQuote

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `reservation` (ForeignKey) null=False blank=False unique=False
- `status` (CharField) null=False blank=False unique=False
- `currency` (CharField) null=False blank=False unique=False
- `subtotal` (DecimalField) null=False blank=False unique=False
- `tax` (DecimalField) null=False blank=False unique=False
- `total` (DecimalField) null=False blank=False unique=False
- `priced_at_utc` (DateTimeField) null=True blank=True unique=False
- `priced_by_user` (ForeignKey) null=True blank=True unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

## pricing.PricingQuoteItem

### Fields
- `created_at` (DateTimeField) null=False blank=True unique=False
- `updated_at` (DateTimeField) null=False blank=True unique=False
- `id` (UUIDField) null=False blank=False unique=True
- `quote` (ForeignKey) null=False blank=False unique=False
- `code` (CharField) null=False blank=False unique=False
- `label` (CharField) null=False blank=False unique=False
- `qty` (DecimalField) null=False blank=False unique=False
- `unit_price` (DecimalField) null=False blank=False unique=False
- `amount` (DecimalField) null=False blank=False unique=False
- `locked` (BooleanField) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `NotUpdated()`

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


# Code inventory: accounts

## accounts/api/serializers.py


## accounts/api/urls.py


## accounts/api/views.py


# Code inventory: availability

## availability/api/serializers.py


## availability/api/urls.py


## availability/api/views.py


# Code inventory: audit

# Code inventory: pricing

# Code inventory: common

## common/auth/permissions.py


# Code inventory: fleet

## fleet/api/serializers.py


## fleet/api/urls.py


## fleet/api/views.py

