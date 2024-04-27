from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from datetime import date

class Calendar(models.Model):
    normal_week_schedule = models.DateField(help_text="Horario normal de la semana")
    summer_week_schedule = models.DateField(help_text="Horario de verano")
    winter_week_schedule = models.DateField(help_text="Horario de invierno")
    normal_start_date = models.DateField(help_text="Fecha de inicio del horario normal")
    summer_start_date = models.DateField(help_text="Fecha de inicio del horario de verano")
    winter_start_date = models.DateField(help_text="Fecha de inicio del horario de invierno")
    closed_days = ArrayField(
        models.DateField(),
        default=list,
        help_text="Lista de días cerrados"
    )

    def __str__():
        """Devuelve una representación simple del calendario"""
        return f'Calendar {self.pk}: Normal {self.normal_start_date}, Verano {self.summer_start_date}, Invierno {self.winter_start_date}'
