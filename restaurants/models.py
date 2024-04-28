import uuid
from django.db import models
from django.utils import timezone
from django.db.models import JSONField
from utils.validators import validate_address
from calendars.models import Calendar

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = JSONField(default=dict, blank=True, validators=[validate_address])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Relación con Calendar
    calendar = models.OneToOneField(
        Calendar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restaurant',
        help_text="El calendario asignado a este restaurante"
    )

    def __str__(self):
        return self.name
