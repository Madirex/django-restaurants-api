from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from restaurants.models import Restaurant
from tables.models import Table
from calendars.models import Calendar
from datetime import timedelta
from django.utils import timezone

class RestaurantTests(TestCase):
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

        # Crear un calendario para usar en los tests
        self.calendar = Calendar.objects.create(
            normal_start_date=timezone.now(),
            summer_start_date=timezone.now() + timedelta(days=30),
            winter_start_date=timezone.now() + timedelta(days=60),
        )

    def test_create_restaurant_as_admin(self):
        """Test para crear un restaurante como administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'name': 'Test Restaurant',
            'address': {
                'street': '123 Main St',
                'city': 'Sample City'
            },
            'calendar': self.calendar.pk,
        }

        response = self.client.post("/restaurants/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Restaurant')

    def test_list_restaurants(self):
        """Test para listar restaurantes"""
        Restaurant.objects.create(
            name='Restaurant One',
            calendar=self.calendar,
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/restaurants/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_restaurant(self):
        """Test para obtener detalles de un restaurante"""
        restaurant = Restaurant.objects.create(
            name='Restaurant One',
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/restaurants/{restaurant.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Restaurant One')

    def test_update_restaurant_as_admin(self):
        """Test para actualizar un restaurante como administrador"""
        restaurant = Restaurant.objects.create(
            name='Restaurant One',
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {'name': 'Updated Restaurant'}

        response = self.client.patch(f"/restaurants/{restaurant.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Restaurant')

    def test_destroy_restaurant_as_admin(self):
        """Test para eliminar un restaurante como administrador"""
        restaurant = Restaurant.objects.create(
            name='Restaurant One',
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.delete(f"/restaurants/{restaurant.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_restaurant_as_standard_user(self):
        """Probar crear un restaurante como usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {
            'name': 'Test Restaurant',
            'address': {
                'street': '123 Main St',
                'city': 'Sample City',
                'state': 'Sample State',
                'zip': '12345',
            },
            'calendar': self.calendar.pk,
        }

        response = self.client.post("/restaurants/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class IncorrectRestaurantTests(TestCase):
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

        # Crear un calendario para usar en los tests
        self.calendar = Calendar.objects.create(
            normal_start_date=timezone.now(),
            summer_start_date=timezone.now() + timedelta(days=30),
            winter_start_date=timezone.now() + timedelta(days=60),
        )

    def test_create_restaurant_with_invalid_address(self):
        """Probar creación de restaurante con una dirección inválida"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'name': 'Invalid Restaurant',
            'address': 'This is not a valid address',
            'calendar': self.calendar.pk,
        }

        response = self.client.post("/restaurants/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_restaurant_without_name(self):
        """Probar creación de restaurante sin nombre (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'address': {
                'street': '123 Main St',
                'city': 'Sample City',
            },
            'calendar': self.calendar.pk,
        }

        response = self.client.post("/restaurants/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_restaurant_with_invalid_name(self):
        """Probar actualización de un restaurante con nombre vacío"""
        restaurant = Restaurant.objects.create(
            name='Valid Restaurant',
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {'name': ''}

        response = self.client.patch(f"/restaurants/{restaurant.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_restaurant_as_standard_user(self):
        """Probar eliminación de un restaurante como usuario estándar (debería fallar)"""
        restaurant = Restaurant.objects.create(
            name='Restaurant to Delete',
            calendar=self.calendar,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        response = self.client.delete(f"/restaurants/{restaurant.pk}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)