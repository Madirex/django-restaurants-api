from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from schedules.models import Schedule
from calendars.models import Calendar

class CalendarTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuario administrador y token
        self.admin_user = User.objects.create_user(
            username='admin23',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            is_admin=True,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        # Crear usuario estándar y token
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

        # Crear un Schedule con un Calendar asociado
        self.schedule = Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar
        )

    def test_create_calendar_as_admin(self):
        """Test para crear un Calendar como administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'normal_week_schedule': self.schedule.pk,
            'normal_start_date': '2024-01-01',
            'summer_start_date': '2024-06-01',
            'winter_start_date': '2024-12-01',
            'closed_days': ['2024-01-01', '2024-12-25'],
        }

        response = self.client.post("/calendars/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['normal_start_date'], '2024-01-01')

    def test_list_calendars(self):
        """Test para listar Calendars"""
        Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/calendars/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_calendar(self):
        """Test para obtener detalles de un Calendar"""
        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/calendars/{calendar.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['normal_start_date'], '2024-01-01')

    def test_update_calendar_as_admin(self):
        """Test para actualizar un Calendar como administrador"""
        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {'normal_start_date': '2024-01-15'}

        response = self.client.patch(f"/calendars/{calendar.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['normal_start_date'], '2024-01-15')

    def test_destroy_calendar_as_admin(self):
        """Test para eliminar un Calendar como administrador"""
        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.delete(f"/calendars/{calendar.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_closed_day_as_admin(self):
        """Test para agregar un día de cierre como administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        data = {'closed_day': '2024-12-31'}

        response = self.client.post(f"/calendars/{calendar.pk}/add-closed-day/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('2024-12-31', response.data['closed_days'])

    def test_remove_closed_day_as_admin(self):
        """Test para eliminar un día de cierre como administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        data = {'closed_day': '2024-12-25'}

        response = self.client.delete(f"/calendars/{calendar.pk}/remove-closed-day/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('2024-12-25', response.data['closed_days'])

class IncorrectCalendarTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuario administrador y token
        self.admin_user = User.objects.create_user(
            username='admin23',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            is_admin=True,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        # Crear usuario estándar y token
        self.standard_user = User.objects.create_user(
            username='standard',
            email='standard@example.com',
            password='standard123',
        )
        self.standard_token = Token.objects.create(user=self.standard_user)

        # Crear un calendario y un horario para las pruebas
        self.calendar = Calendar.objects.create(
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01'
        )

        self.schedule = Schedule.objects.create(
            day='2024-01-01',
            opened_hours=['08:00', '18:00'],
            calendar=self.calendar
        )

    def test_create_calendar_as_standard_user(self):
        """Intentar crear un calendario como usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {
            'normal_week_schedule': self.schedule.pk,
            'normal_start_date': '2024-01-01',
            'summer_start_date': '2024-06-01',
            'winter_start_date': '2024-12-01',
            'closed_days': ['2024-01-01', '2024-12-25'],
        }

        response = self.client.post("/calendars/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_calendar_as_standard_user(self):
        """Intentar actualizar un calendario como usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {'normal_start_date': '2024-01-15'}

        response = self.client.patch(f"/calendars/{self.calendar.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_calendar_as_standard_user(self):
        """Intentar eliminar un calendario como usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        response = self.client.delete(f"/calendars/{self.calendar.pk}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_calendar_with_invalid_data(self):
        """Intentar crear un calendario con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'normal_week_schedule': 999,
            'normal_start_date': '2024-01-01',
            'summer_start_date': '2024-06-01',
            'winter_start_date': '2024-12-01',
            'closed_days': ['2024-01-01', '2024-12-25'],
        }

        response = self.client.post("/calendars/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_non_existent_calendar(self):
        """Intentar obtener un calendario inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/calendars/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_closed_day_with_invalid_date(self):
        """Test para agregar un día de cierre con una fecha inválida"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        data = {'closed_day': 'invalid-date'}

        response = self.client.post(f"/calendars/{calendar.pk}/add-closed-day/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Formato de fecha inválido.')

    def test_add_closed_day_as_standard_user(self):
        """Test para agregar un día de cierre como usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        data = {'closed_day': '2024-12-31'}

        response = self.client.post(f"/calendars/{calendar.pk}/add-closed-day/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_closed_day_with_invalid_date(self):
        """Test para eliminar un día de cierre con una fecha inválida"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        data = {'closed_day': 'invalid-date'}

        response = self.client.delete(f"/calendars/{calendar.pk}/remove-closed-day/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Formato de fecha inválido. Use YYYY-MM-DD.')

    def test_remove_closed_day_as_standard_user(self):
        """Test para eliminar un día de cierre como usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        calendar = Calendar.objects.create(
            normal_week_schedule=self.schedule,
            normal_start_date='2024-01-01',
            summer_start_date='2024-06-01',
            winter_start_date='2024-12-01',
            closed_days=['2024-01-01', '2024-12-25'],
        )

        data = {'closed_day': '2024-12-25'}

        response = self.client.delete(f"/calendars/{calendar.pk}/remove-closed-day/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)