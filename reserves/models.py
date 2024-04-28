from django.db import models
from django.core.validators import MinValueValidator
from restaurants.models import Restaurant
from orders.models import Order
from uuid import uuid4
from tables.models import Table

class Reserve(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    start_reserve = models.DateTimeField()
    finish_reserve = models.DateTimeField()
    assigned_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='reserves'
    )
    assigned_chairs = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    table = models.ForeignKey(
        'tables.Table',
        on_delete=models.CASCADE,
        related_name='reserves'
    )

    def __str__(self):
        return f'Reserva de {self.start_reserve} a {self.finish_reserve} en la mesa {self.table.id}, con {self.assigned_chairs} sillas.'
