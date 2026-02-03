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

# Code inventory: accounts

## accounts/api/serializers.py


## accounts/api/urls.py


## accounts/api/views.py

