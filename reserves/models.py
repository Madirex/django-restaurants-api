from django.db import models
from django.core.validators import MinValueValidator
from restaurants.models import Restaurant
from orders.models import Order
from uuid import uuid4
from tables.models import Table
from datetime import timedelta

class Reserve(models.Model):
    """Modelo para representar una reserva."""
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

    def clean(self):
        """Validar que no haya reservas que se superpongan para la misma mesa"""
        overlapping_reservations = Reserve.objects.filter(
            table=self.table,
            start_reserve__lt=self.finish_reserve - timedelta(minutes=5),
            finish_reserve__gt=self.start_reserve,
        ).exclude(assigned_order__status='cancelled')

        if self.id:  # Si estamos actualizando, excluir la reserva actual
            overlapping_reservations = overlapping_reservations.exclude(id=self.id)

        if overlapping_reservations.exists():
            raise ValidationError("Ya existe una reserva que se superpone con el rango de tiempo especificado.")

    def save(self, *args, **kwargs):
        """Aplicar la validación antes de guardar la reserva"""
        self.clean()  # Validar antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        """Devuelve la representación en string de la reserva."""
        return f'Reserva de {self.start_reserve} a {self.finish_reserve} en la mesa {self.table.id}, con {self.assigned_chairs} sillas.'
