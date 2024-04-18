from django.db import models
from dishes.models import Dish
import uuid

class RestaurantDishLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    #restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='linked_restaurants')
    stock = models.IntegerField()

    def __str__(self):
        """Return a string representation"""
        return f'{self.dish}'
