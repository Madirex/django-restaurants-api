from django.db import models
from users.models import User

# django-ckeditor
from ckeditor.fields import RichTextField

class Category(models.Model):
    # TODO: ENLAZAR CON PLATO (DISH) -- user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return name"""
        return f'{self.name}'