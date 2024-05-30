from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from cartcodes.models import CartCode
from rest_framework.authtoken.models import Token

class CartCodeTests(TestCase):
    """Test para el modelo CartCode"""
    def setUp(self):
        """Configuración inicial de los tests"""
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

    def test_create_cart_code_as_admin(self):
        """Test para crear un código de carrito con un administrador"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        # Datos para crear un CartCode
        data = {
            'code': 'DISCOUNT2024',
            'is_active': True,
            'percent_discount': 10,
            'fixed_discount': 0,
            'available_uses': 5,
            'expiration_date': None,
        }

        response = self.client.post('/cartcodes/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 'DISCOUNT2024')

    def test_list_cart_codes_as_admin(self):
        """Test para listar códigos de carrito como administrador"""
        CartCode.objects.create(
            code='CODE1',
            is_active=True,
            percent_discount=10,
            fixed_discount=0,
            available_uses=10,
            expiration_date=None
        )
        CartCode.objects.create(
            code='CODE2',
            is_active=True,
            percent_discount=0,
            fixed_discount=5,
            available_uses=5,
            expiration_date=None
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        response = self.client.get('/cartcodes/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_cart_code(self):
        """Test para obtener detalles de un código de carrito"""
        cart_code = CartCode.objects.create(
            code='TESTCODE',
            is_active=True,
            percent_discount=10,
            fixed_discount=0,
            available_uses=5,
            expiration_date=None
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        response = self.client.get(f'/cartcodes/{cart_code.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'TESTCODE')

    def test_update_cart_code_as_admin(self):
        """Test para actualizar un código de carrito con un administrador"""
        cart_code = CartCode.objects.create(
            code='OLDCODE',
            is_active=True,
            percent_discount=10,
            fixed_discount=0,
            available_uses=5,
            expiration_date=None
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        data = {
            'code': 'NEWCODE',
            'is_active': True,
            'percent_discount': 15,
            'fixed_discount': 0,
            'available_uses': 5,
        }

        response = self.client.patch(f'/cartcodes/{cart_code.pk}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'NEWCODE')

    def test_destroy_cart_code_as_admin(self):
        """Test para eliminar un código de carrito con un administrador"""
        cart_code = CartCode.objects.create(
            code='DELETECODE',
            is_active=True,
            percent_discount=10,
            fixed_discount=0,
            available_uses=5,
            expiration_date=None
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        response = self.client.delete(f'/cartcodes/{cart_code.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_cart_code_as_standard_user(self):
        """Test para crear un código de carrito con un usuario estándar"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        # Datos para crear un CartCode
        data = {
            'code': 'DISCOUNT2024',
            'is_active': True,
            'percent_discount': 10,
            'fixed_discount': 0,
            'available_uses': 5,
            'expiration_date': None,
        }

        response = self.client.post('/cartcodes/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from cartcodes.models import CartCode
from rest_framework.authtoken.models import Token

class IncorrectCartCodeTests(TestCase):
    """Test para el modelo CartCode"""
    def setUp(self):
        """Configuración inicial de los tests"""
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

    def test_create_cart_code_as_standard_user(self):
        """Probar creación de código de carrito con usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = "/cartcodes/"

        data = {
            'code': 'UNAUTHORIZEDCODE',
            'is_active': True,
            'percent_discount': 10,
            'fixed_discount': 0,
            'available_uses': 5,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_cart_code_with_invalid_data(self):
        """Probar creación de código de carrito con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        url = "/cartcodes/"

        data = {
            'code': '',
            'is_active': True,
            'percent_discount': -10,
            'fixed_discount': -5,
            'available_uses': -1,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_cart_code_as_standard_user(self):
        """Probar actualización de código de carrito con usuario estándar (debería fallar)"""
        cart_code = CartCode.objects.create(
            code='CODE123',
            is_active=True,
            percent_discount=10,
            fixed_discount=0,
            available_uses=5,
            expiration_date=None,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = f"/cartcodes/{cart_code.pk}/"

        data = {'code': 'NEWCODE123'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_cart_code_as_standard_user(self):
        """Probar eliminación de código de carrito con usuario estándar (debería fallar)"""
        cart_code = CartCode.objects.create(
            code='DELETECODE',
            is_active=True,
            percent_discount=10,
            fixed_discount=0,
            available_uses=5,
            expiration_date=None,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = f"/cartcodes/{cart_code.pk}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_non_existent_cart_code(self):
        """Probar recuperación de código de carrito inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        url = "/cartcodes/999/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
