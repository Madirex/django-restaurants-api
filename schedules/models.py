from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, time
from utils.validators import validate_half_hour

class Schedule(models.Model):
    """Modelo para horarios"""

    day = models.DateField(help_text="Día del horario")

    opened_hours = ArrayField(
        models.TimeField(),
        default=list,
        help_text="Lista de horas de apertura",
        validators=[validate_half_hour]
    )

    calendar = models.ForeignKey(
        'calendars.Calendar',
        on_delete=models.CASCADE,
        related_name='customs_schedules',
        help_text="El calendario asociado"
    )

    def __str__(self):
        return f"Schedule para {self.day}"
