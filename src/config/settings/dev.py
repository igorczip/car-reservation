# src/config/settings/dev.py
from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]

print("✅ DJANGO_SETTINGS_MODULE:", "config.settings.dev")
print("✅ DB ENGINE:", DATABASES["default"]["ENGINE"])
print("✅ DB HOST:", DATABASES["default"].get("HOST"))
print("✅ DB NAME:", DATABASES["default"].get("NAME"))
