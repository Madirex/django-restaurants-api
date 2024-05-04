from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from schedules.models import Schedule
from calendars.models import Calendar

class ScheduleTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear un usuario administrador
        self.admin_user = User.objects.create_user(
            username='admin23',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            is_admin=True,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        # Crear un usuario estándar
        self.standard_user = User.objects.create_user(
            username='standard',
            email='standard@example.com',
            password='standard123',
        )
        self.standard_token = Token.objects.create(user=self.standard_user)

        # Crear un Calendar para asociar con Schedule
        self.calendar = Calendar.objects.create(
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01'
        )

    def test_create_schedule_as_admin(self):
        """Test para crear un Schedule como administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'day': '2024-01-01',
            'opened_hours': ['08:00', '18:00'],
            'calendar': self.calendar.pk,
        }

        response = self.client.post("/schedules/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['day'], '2024-01-01')

    def test_list_schedules(self):
        """Test para listar Schedules"""
        Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/schedules/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_schedule(self):
        """Test para obtener detalles de un Schedule"""
        schedule = Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/schedules/{schedule.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['day'], '2024-01-01')

    def test_update_schedule_as_admin(self):
        """Test para actualizar un Schedule como administrador"""
        schedule = Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {'day': '2024-01-15', 'calendar': self.calendar.pk}


        response = self.client.patch(f"/schedules/{schedule.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['day'], '2024-01-15')

    def test_destroy_schedule_as_admin(self):
        """Test para eliminar un Schedule como administrador"""
        schedule = Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.delete(f"/schedules/{schedule.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class IncorrectScheduleTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuario administrador
        self.admin_user = User.objects.create_user(
            username='admin23',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            is_admin=True,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        # Crear usuario estándar
        self.standard_user = User.objects.create_user(
            username='standard',
            email='standard@example.com',
            password='standard123',
        )
        self.standard_token = Token.objects.create(user=self.standard_user)

        # Crear un Calendar para asociar con Schedule
        self.calendar = Calendar.objects.create(
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01'
        )

    def test_create_schedule_with_invalid_data(self):
        """Intentar crear un Schedule con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'day': '',
            'opened_hours': ['25:00'],
            'calendar': self.calendar.pk,
        }

        response = self.client.post("/schedules/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_schedule_as_standard_user(self):
        """Intentar crear un Schedule como usuario estándar"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {
            'day': '2024-01-01',
            'opened_hours': ['08:00', '18:00'],
            'calendar': self.calendar.pk,
        }

        response = self.client.post("/schedules/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_schedule_as_standard_user(self):
        """Intentar actualizar un Schedule como usuario estándar"""
        schedule = Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {'day': '2024-01-15'}

        response = self.client.patch(f"/schedules/{schedule.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_non_existent_schedule(self):
        """Intentar recuperar un Schedule inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/schedules/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_schedule_as_standard_user(self):
        """Intentar eliminar un Schedule como usuario estándar"""
        schedule = Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        response = self.client.delete(f"/schedules/{schedule.pk}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)