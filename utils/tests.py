from django.test import TestCase
from datetime import datetime, date
from schedules.models import Schedule
from rest_framework.exceptions import ValidationError
from utils.calendar_utils import get_schedule_for_day
from calendars.models import Calendar
from reserves.models import Reserve
from utils.calendar_utils import get_occupied_hours, get_available_hours

from django.test import TestCase
from datetime import datetime, date, time
from schedules.models import Schedule
from rest_framework.exceptions import ValidationError
from utils.calendar_utils import get_schedule_for_day
from calendars.models import Calendar
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.validators import (
    validate_address,
    validate_half_hour,
    validate_unique_schedule_day,
)

class ScheduleUtilsTests(TestCase):
    """Pruebas para las utilidades de Schedule."""
    def setUp(self):
        """Configuración de las pruebas."""
        self.calendar = Calendar.objects.create(
            normal_start_date=date(2022, 1, 1),
            summer_start_date=date(2022, 6, 1),
            winter_start_date=date(2022, 12, 1),
        )

        self.normal_schedule = Schedule.objects.create(
            calendar=self.calendar,
            day=date(2022, 1, 2),
            opened_hours=["08:00:00", "12:00:00", "18:00:00"],
        )

        self.summer_schedule = Schedule.objects.create(
            calendar=self.calendar,
            day=date(2022, 6, 2),
            opened_hours=["09:00:00", "13:00:00", "19:00:00"],
        )

        self.winter_schedule = Schedule.objects.create(
            calendar=self.calendar,
            day=date(2022, 12, 2),
            opened_hours=["10:00:00", "14:00:00", "20:00:00"],
        )

    def test_get_schedule_for_day_normal(self):
        """Prueba para obtener el horario en un día normal"""
        day = date(2022, 1, 2)
        schedule = get_schedule_for_day(self.calendar, day)
        self.assertEqual(schedule, self.normal_schedule)

    def test_get_schedule_for_day_summer(self):
        """Prueba para obtener el horario en un día de verano"""
        day = date(2022, 6, 2)
        schedule = get_schedule_for_day(self.calendar, day)
        self.assertEqual(schedule, self.summer_schedule)

    def test_get_schedule_for_day_winter(self):
        """Prueba para obtener el horario en un día de invierno"""
        day = date(2022, 12, 2)
        schedule = get_schedule_for_day(self.calendar, day)
        self.assertEqual(schedule, self.winter_schedule)

class AvailableHoursTests(TestCase):
    def setUp(self):
        """Configuración de las pruebas."""
        self.opening_hours = ["08:00:00", "10:00:00", "12:00:00", "14:00:00"]
        self.occupied_hours = {"10:00:00", "12:00:00"}

    def test_get_available_hours(self):
        """Prueba para verificar las horas disponibles"""
        available_hours = get_available_hours(self.opening_hours, self.occupied_hours)

        self.assertListEqual(
            available_hours,
            ["08:00:00", "14:00:00"],
            "Las horas disponibles no coinciden"
        )

class ValidateAddressTests(TestCase):
    def test_validate_address_valid(self):
        """Prueba para una dirección válida"""
        address = {
            "street": "Calle Falsa",
            "number": "123",
            "city": "Madrid",
            "province": "Madrid",
            "country": "España",
            "postal_code": "28001",
        }
        try:
            validate_address(address)
        except ValidationError:
            self.fail("No se esperaba ValidationError para una dirección válida.")

    def test_validate_address_invalid_type(self):
        """Prueba para una dirección que no es un objeto JSON"""
        address = "Not a JSON object"
        with self.assertRaises(ValidationError):
            validate_address(address)

    def test_validate_address_unexpected_fields(self):
        """Prueba para campos inesperados en la dirección"""
        address = {
            "unexpected_field": "Unexpected",
            "city": "Madrid",
        }
        with self.assertRaises(ValidationError) as context:
            validate_address(address)

        self.assertIn(
            "Los siguientes campos no están permitidos: unexpected_field",
            str(context.exception),
        )

    def test_validate_address_exceed_max_length(self):
        """Prueba para campos que exceden la longitud máxima"""
        long_street = "A" * 101
        address = {
            "street": long_street,
            "city": "Madrid",
        }
        with self.assertRaises(ValidationError) as context:
            validate_address(address)

        self.assertIn(
            "El campo 'street' no debe exceder 100 caracteres.",
            str(context.exception),
        )

class ValidateHalfHourTests(TestCase):
    def test_validate_half_hour_valid(self):
        """Prueba para tiempos correctos"""
        valid_times = [time(8, 0), time(9, 30), time(10, 0)]
        try:
            validate_half_hour(valid_times)
        except ValidationError:
            self.fail("No se esperaba ValidationError para tiempos válidos.")

    def test_validate_half_hour_invalid(self):
        """Prueba para tiempos incorrectos"""
        invalid_times = [time(8, 15), time(9, 45)]
        with self.assertRaises(ValidationError) as context:
            validate_half_hour(invalid_times)

        self.assertIn(
            "Las horas de apertura deben ser cada media hora",
            str(context.exception),
        )

class ValidateUniqueScheduleDayTests(TestCase):
    """Validar que no exista un horario para un día en el calendario"""
    def setUp(self):
        """Configuración de las pruebas."""
        self.calendar = Calendar.objects.create(
            normal_start_date=date(2022, 1, 1),
            summer_start_date=date(2022, 6, 1),
            winter_start_date=date(2022, 12, 1),
        )

        self.schedule = Schedule.objects.create(
            calendar=self.calendar,
            day=date(2022, 1, 2),
            opened_hours=["08:00:00"],
        )

    def test_validate_unique_schedule_day_valid(self):
        """Prueba para una validación única válida"""
        try:
            validate_unique_schedule_day(
                self.calendar.customs_schedules, date(2022, 1, 3), self.schedule.id
            )
        except ValidationError:
            self.fail("No se esperaba ValidationError para una validación única válida.")

    def test_validate_unique_schedule_day_existing(self):
        """Prueba para una fecha que ya existe en el calendario"""
        with self.assertRaises(ValidationError) as context:
            validate_unique_schedule_day(
                self.calendar.customs_schedules, self.schedule.day
            )

        self.assertIn(
            "Ya existe un horario para el día", str(context.exception),
            "El mensaje de error no es el esperado",
        )