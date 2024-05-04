from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from restaurants.models import Restaurant
from tables.models import Table

class TableTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            username='admin23',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            is_admin=True,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.standard_user = User.objects.create_user(
            username='standard',
            email='standard@example.com',
            password='standard123',
        )
        self.standard_token = Token.objects.create(user=self.standard_user)

        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

    def test_create_table_as_admin(self):
        """Test para crear una mesa con un administrador"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        data = {
            'x_position': 1,
            'y_position': 2,
            'min_chairs': 2,
            'max_chairs': 4,
            'assigned_restaurant': self.restaurant.pk,
            'is_active': True,
        }

        response = self.client.post('/tables/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['x_position'], 1)

    def test_create_table_with_invalid_data(self):
        """Probar creación de mesa con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        data = {
            'x_position': 1,
            'y_position': 2,
            'min_chairs': 5,
            'max_chairs': 3,
            'assigned_restaurant': self.restaurant.pk,
            'is_active': True,
        }

        response = self.client.post('/tables/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_table_with_missing_data(self):
        """Probar creación de mesa con datos faltantes"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        data = {
            'x_position': 1,
            'y_position': 2,
            'assigned_restaurant': self.restaurant.pk,
            'is_active': True,
        }

        response = self.client.post('/tables/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_table_as_admin(self):
        """Test para crear una mesa con un administrador"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        data = {
            'x_position': 1,
            'y_position': 2,
            'min_chairs': 2,
            'max_chairs': 4,
            'assigned_restaurant': self.restaurant.pk,
            'is_active': True,
        }

        response = self.client.post('/tables/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_table_as_standard_user(self):
        """Probar eliminación de mesa por usuario estándar (debería fallar)"""
        table = Table.objects.create(
            x_position=1,
            y_position=2,
            min_chairs=2,
            max_chairs=4,
            assigned_restaurant=self.restaurant,
            is_active=True,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        response = self.client.delete(f'/tables/{table.pk}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)