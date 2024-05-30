import uuid
from django.db import models
from django.utils import timezone
from django.db.models import JSONField
from utils.validators import validate_address
from calendars.models import Calendar

class Restaurant(models.Model):
    """Modelo para representar un restaurante."""
    name = models.CharField(max_length=255)
    address = JSONField(default=dict, blank=True, validators=[validate_address])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Relación con Calendar
    calendar = models.OneToOneField(
        Calendar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restaurant',
        help_text="El calendario asignado a este restaurante"
    )

    def __str__(self):
        """Return a string representation"""
        return self.name

    def delete(self, *args, **kwargs):
        """Eliminar un restaurante"""
        # Eliminar el calendario asociado con todos sus horarios
        # NOTE: Esto se hace para simplificar el proyecto. En un futuro se podría eliminar y hacer que cada calendar/schedule se pueda reciclar en otros restaurantes
        if self.calendar:
            # Eliminar customs_schedules
            self.calendar.customs_schedules.all().delete()

            # Eliminar normal_week_schedule, summer_week_schedule, winter_week_schedule
            for schedule in [self.calendar.normal_week_schedule, self.calendar.summer_week_schedule, self.calendar.winter_week_schedule]:
                if schedule:
                    schedule.delete()

        # Eliminar calendario
        if self.calendar:
            self.calendar.delete()

        super().delete(*args, **kwargs)
