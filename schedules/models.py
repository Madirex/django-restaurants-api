from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, time
from calendars.models import Calendar

class Schedule(models.Model):
    """Modelo para horarios"""

    day = models.DateField(help_text="Día del horario")

    opened_hours = ArrayField(
        models.TimeField(),
        default=list,
        help_text="Lista de horas de apertura"
    )

    closed_hours = ArrayField(
        models.TimeField(),
        default=list,
        help_text="Lista de horas de cierre"
    )

    calendar = models.ForeignKey(
        'calendars.Calendar',
        on_delete=models.CASCADE,
        related_name='schedules',
        help_text="El calendario asociado"
    )

    # Añadir alguna validación para asegurar que la lista de horas de cierre coincida con la de apertura
    def clean(self):
        if len(self.opened_hours) != len(self.closed_hours):
            raise ValidationError("El número de horas de apertura debe coincidir con el de cierre.")

        # Puedes añadir otras validaciones para asegurarte de que las horas de cierre son después de las horas de apertura
        for open_time, close_time in zip(self.opened_hours, self.closed_hours):
            if open_time >= close_time:
                raise ValidationError("Cada hora de apertura debe ser antes de la hora de cierre correspondiente.")

    def __str__(self):
        return f"Schedule para {self.day}"
