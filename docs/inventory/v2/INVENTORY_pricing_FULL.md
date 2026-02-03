✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation
✅ DJANGO_SETTINGS_MODULE: config.settings.dev
✅ DB ENGINE: django.db.backends.postgresql
✅ DB HOST: db
✅ DB NAME: car_reservation

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

# Code inventory: pricing
