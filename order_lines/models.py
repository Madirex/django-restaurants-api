import uuid
from django.db import models
from django.core.validators import MinValueValidator
from dishes.models import Dish
from orders.models import Order

class OrderLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selected = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        self.subtotal = self.total
        super().save(*args, **kwargs)

    def __str__(self):
        return f'OrderLine {self.id}: {self.quantity}x {self.dish.name} (${self.total})'
