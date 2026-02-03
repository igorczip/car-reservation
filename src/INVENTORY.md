✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation

## admin.LogEntry

### Fields
- `id` (AutoField) null=False blank=True unique=True
- `action_time` (DateTimeField) null=False blank=False unique=False
- `user` (ForeignKey) null=False blank=False unique=False
- `content_type` (ForeignKey) null=True blank=True unique=False
- `object_id` (TextField) null=True blank=True unique=False
- `object_repr` (CharField) null=False blank=False unique=False
- `action_flag` (PositiveSmallIntegerField) null=False blank=False unique=False
- `change_message` (TextField) null=False blank=True unique=False

### Properties
- (žádné)

### Methods
- `DoesNotExist()`
- `MultipleObjectsReturned()`
- `NotUpdated()`
- `get_admin_url()` – Return the admin URL to edit the object represented by this log entry.
- `get_change_message()` – If self.change_message is a JSON structure, interpret it as a change
- `get_edited_object()` – Return the edited object represented by this log entry.
- `is_addition()`
- `is_change()`
- `is_deletion()`

## auth.Permission

### Fields
- `id` (AutoField) null=False blank=True unique=True
- `name` (CharField) null=False blank=False unique=False
- `content_type` (ForeignKey) null=False blank=False unique=False
- `codename` (CharField) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `DoesNotExist()`
- `MultipleObjectsReturned()`
- `NotUpdated()`
- `natural_key()`

## auth.Group

### Fields
- `id` (AutoField) null=False blank=True unique=True
- `name` (CharField) null=False blank=False unique=True
- `permissions` (ManyToManyField) null=False blank=True unique=False

### Properties
- (žádné)

### Methods
- `DoesNotExist()`
- `MultipleObjectsReturned()`
- `NotUpdated()`
- `natural_key()`

## auth.User

### Fields
- `id` (AutoField) null=False blank=True unique=True
- `password` (CharField) null=False blank=False unique=False
- `last_login` (DateTimeField) null=True blank=True unique=False
- `is_superuser` (BooleanField) null=False blank=False unique=False
- `username` (CharField) null=False blank=False unique=True
- `first_name` (CharField) null=False blank=True unique=False
- `last_name` (CharField) null=False blank=True unique=False
- `email` (EmailField) null=False blank=True unique=False
- `is_staff` (BooleanField) null=False blank=False unique=False
- `is_active` (BooleanField) null=False blank=False unique=False
- `date_joined` (DateTimeField) null=False blank=False unique=False
- `groups` (ManyToManyField) null=False blank=True unique=False
- `user_permissions` (ManyToManyField) null=False blank=True unique=False

### Properties
- (žádné)

### Methods
- `DoesNotExist()`
- `MultipleObjectsReturned()`
- `NotUpdated()`

## contenttypes.ContentType

### Fields
- `id` (AutoField) null=False blank=True unique=True
- `app_label` (CharField) null=False blank=False unique=False
- `model` (CharField) null=False blank=False unique=False

### Properties
- `app_labeled_name` (property)
- `name` (property)

### Methods
- `DoesNotExist()`
- `MultipleObjectsReturned()`
- `NotUpdated()`
- `get_all_objects_for_this_type()` – Return all objects of this type for the keyword arguments given.
- `get_object_for_this_type()` – Return an object of this type for the keyword arguments given.
- `model_class()` – Return the model class for this type of content.
- `natural_key()`

## sessions.Session

### Fields
- `session_key` (CharField) null=False blank=False unique=True
- `session_data` (TextField) null=False blank=False unique=False
- `expire_date` (DateTimeField) null=False blank=False unique=False

### Properties
- (žádné)

### Methods
- `DoesNotExist()`
- `MultipleObjectsReturned()`
- `NotUpdated()`
- `get_session_store_class()`

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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
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
- `DoesNotExist()`
- `MultipleObjectsReturned()`
- `NotUpdated()`
