from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.apps import AppConfig
from django.db.models import JSONField
from address.validators import validate_address

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    modified = models.DateTimeField(auto_now=True)
    photo = models.ImageField(null=True, upload_to='users')
    phone = models.CharField(null=True, max_length=15)
    is_admin = models.BooleanField(default=False)
    address = JSONField(default=dict, blank=True, validators=[validate_address])

    def save(self, *args, **kwargs):
        validate_address(self.address)  # Validar Address antes de guardar
        super().save(*args, **kwargs)