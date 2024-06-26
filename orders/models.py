import uuid
from django.db import models
from django.core.validators import MinValueValidator
from restaurants.models import Restaurant
from users.models import User
from cartcodes.models import CartCode

class OrderStatus(models.TextChoices):
    """Clase para representar los estados de un pedido."""
    PENDING = 'pending', 'Pendiente'
    CONFIRMED = 'confirmed', 'Confirmada'
    CANCELLED = 'cancelled', 'Cancelada'
    COMPLETED = 'completed', 'Completada'

class Order(models.Model):
    """Modelo para representar un pedido."""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    total_dishes = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    cart_code = models.ForeignKey(CartCode, null=True, on_delete=models.SET_NULL, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Devuelve la representación en string del pedido."""
        return f"Order {self.pk} - {self.status}"

