from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from django.db.models import JSONField
from categories.models import Category

class Dish(models.Model):
    class DishType(models.TextChoices):
        APPETIZER = 'APPETIZER', 'Appetizer'
        MAIN_COURSE = 'MAIN_COURSE', 'Main Course'
        DESSERT = 'DESSERT', 'Dessert'
        DRINK = 'DRINK', 'Drink'
        OTHER = 'OTHER', 'Other'

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    dish_type = models.CharField(max_length=20, choices=DishType.choices)
    ingredients = JSONField(default=list)
    calories = models.FloatField(validators=[MinValueValidator(0)])
    image = models.ImageField(null=True, upload_to='dishes')
    preparation_time = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    category = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return name, description, price, dish_type, ingredients, calories, image, preparation_time, category"""
        return f'{self.name}, {self.description}, {self.price}, {self.dish_type}, {self.ingredients}, {self.calories}, {self.image}, {self.preparation_time}, {self.category}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)