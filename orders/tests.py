from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from restaurants.models import Restaurant
from dishes.models import Dish
from orders.models import Order, OrderStatus
from cartcodes.models import CartCode
from decimal import Decimal

class OrderTests(TestCase):
    # Configuración de la clase de prueba
    def setUp(self):
        self.client = APIClient()
        # Usuarios, restaurantes, y otros datos necesarios
        self.admin_user = User.objects.create_user(
            username='admin23',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            is_admin=True,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        self.dish = Dish.objects.create(
            name="Pizza Margherita",
            description="Classic Italian pizza",
            price=9.99,
            dish_type="MAIN_COURSE",
            is_active=True,
            calories=400,
            preparation_time=20,
        )

    def test_create_order_as_admin(self):
        """Test para crear un Order como administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'restaurant': self.restaurant.pk,
            'user': self.admin_user.pk,
            'total': 100,
            'total_dishes': 10,
            'status': OrderStatus.PENDING,
        }

        response = self.client.post("/orders/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self):
        """Test para obtener detalles de un Order"""
        order = Order.objects.create(
            restaurant=self.restaurant,
            user=self.admin_user,
            total=100,
            total_dishes=10,
            status=OrderStatus.PENDING,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/orders/{order.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_as_admin(self):
        """Test para actualizar un Order como administrador"""
        order = Order.objects.create(
            restaurant=self.restaurant,
            user=self.admin_user,
            total=100,
            total_dishes=10,
            status=OrderStatus.PENDING,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {'total': 100}

        response = self.client.patch(f"/orders/{order.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class IncorrectOrderTests(TestCase):
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

        # Crear un restaurante y un plato para las pruebas
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.dish = Dish.objects.create(
            name="Pizza Margherita",
            description="Classic Italian pizza",
            price=9.99,
            dish_type="MAIN_COURSE",
            is_active=True,
            calories=400,
            preparation_time=20,
        )

    def test_create_order_as_standard_user(self):
        """Probar creación de un Order con usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {
            'restaurant': self.restaurant.pk,
            'user': self.standard_user.pk,
            'total': 100,
            'total_dishes': 10,
            'status': OrderStatus.PENDING,
        }

        response = self.client.post("/orders/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_order_as_standard_user(self):
        """Probar actualización de un Order con usuario estándar (debería fallar)"""
        order = Order.objects.create(
            restaurant=self.restaurant,
            user=self.admin_user,
            total=100,
            total_dishes=10,
            status=OrderStatus.PENDING,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {'total': 120}

        response = self.client.patch(f"/orders/{order.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_non_existent_order(self):
        """Probar recuperación de un Order inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/orders/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
