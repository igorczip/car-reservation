# src/common/models.py
import uuid
from django.db import models


class TimeStampedModel(models.Model):
    """Společný základ: created_at / updated_at pro většinu entit."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Společný základ: UUID primární klíč."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
