import uuid
from django.db import models
from django.utils import timezone
from django.db.models import JSONField
from address.validators import validate_address

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = JSONField(default=dict, blank=True, validators=[validate_address])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
