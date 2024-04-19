import uuid
from django.db import models
from django.utils import timezone

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.UUIDField()
    # TODO: menu
    # TODO: tables -- tables = models.JSONField(default=list)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
