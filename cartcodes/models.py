from django.db import models
from ckeditor.fields import RichTextField
import uuid

class CartCode(models.Model):
    """Modelo de códigos de carrito."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    percent_discount = models.FloatField()
    fixed_discount = models.FloatField()
    available_uses = models.IntegerField()
    expiration_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return id, code, percent_discount, fixed_discount, available_uses, expiration_date"""
        return f'{self.id}, {self.code}, {self.percent_discount}, {self.fixed_discount}, {self.available_uses}, {self.expiration_date}'