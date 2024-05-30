from django.db import models
from users.models import User

# django-ckeditor
from ckeditor.fields import RichTextField

class Category(models.Model):
    """Modelo de categorías."""
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""
        unique_together = [['name']]

    def __str__(self):
        """Return name"""
        return f'{self.name}'