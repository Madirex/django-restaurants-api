from django.db import models
from dishes.models import Dish
from restaurants.models import Restaurant
import uuid

class RestaurantDishLink(models.Model):
    """Modelo para representar la relación entre un restaurante y un plato."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='restaurants')
    stock = models.IntegerField()

    def __str__(self):
        """Return a string representation"""
        return f'{self.dish}'
