from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, time
from utils.validators import validate_half_hour, validate_unique_schedule_day

class Schedule(models.Model):
    """Modelo para horarios"""

    day = models.DateField(help_text="Día del horario", null=True, blank=True)

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

    def clean(self):
        """Validar que el día no se repita en el calendario."""
        if self.calendar:
            schedule_queryset = self.calendar.customs_schedules
            validate_unique_schedule_day(schedule_queryset, self.day, self.id)

    def save(self, *args, **kwargs):
        """Validar y guardar el objeto."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Representación en string."""
        return f"Schedule para {self.day}"
