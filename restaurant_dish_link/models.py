from django.db import models
from dishes.models import Dish
from restaurants.models import Restaurant
import uuid

class RestaurantDishLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='restaurants')
    stock = models.IntegerField()

    def __str__(self):
        """Return a string representation"""
        return f'{self.dish}'

        #TODO: instrucciones para usar las relaciones desde Dish o Restaurant:
        ## Supongamos que tenemos un plato específico
        #dish = Dish.objects.get(pk=1)
        #
        ## Accede a los restaurantes vinculados a este plato
        #linked_restaurants = dish.linked_restaurants.all()
        #
        ## Itera sobre los restaurantes vinculados
        #for restaurant in linked_restaurants:
        #    print(restaurant)
