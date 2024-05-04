from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from dishes.models import Dish
from orders.models import Order
from order_lines.models import OrderLine
from restaurants.models import Restaurant

class OrderLineTests(TestCase):
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

        # Crear un restaurante y un pedido para usar en los tests
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        # Crear un pedido y un plato para usar en los tests
        self.order = Order.objects.create(
            restaurant=self.restaurant,
            total=100,
            total_dishes=10,
            status="PENDING",
            user=self.admin_user,
        )

        self.dish = Dish.objects.create(
            name="Pizza Margherita",
            description="Classic Italian pizza",
            price=9.99,
            dish_type="MAIN_COURSE",
            ingredients=["Dough", "Tomato", "Mozzarella", "Basil"],
            calories=400,
            preparation_time=20,
            category="Italian Food",
            is_active=True,
        )

    def test_create_order_line_as_admin(self):
        """Test para crear una línea de pedido con un administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            "quantity": 3,
            "dish": self.dish.pk,
            "order": self.order.pk,
            "price": self.dish.price,
            "selected": True,
        }

        response = self.client.post("/order_lines/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"], 3)
        self.assertEqual(response.data["dish"], self.dish.pk)

    def test_list_order_lines(self):
        """Test para listar las líneas de pedido"""
        OrderLine.objects.create(
            quantity=3,
            dish=self.dish,
            order=self.order,
            price=self.dish.price,
            total=self.dish.price * 3,
            subtotal=self.dish.price * 3,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/order_lines/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_order_line(self):
        """Test para obtener detalles de una línea de pedido"""
        order_line = OrderLine.objects.create(
            quantity=3,
            dish=self.dish,
            order=self.order,
            price=self.dish.price,
            total=self.dish.price * 3,
            subtotal=self.dish.price * 3,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/order_lines/{order_line.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 3)

    def test_update_order_line_as_admin(self):
        """Test para actualizar una línea de pedido con un administrador"""
        order_line = OrderLine.objects.create(
            quantity=3,
            dish=self.dish,
            order=self.order,
            price=self.dish.price,
            total=self.dish.price * 3,
            subtotal=self.dish.price * 3,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {"quantity": 5}

        response = self.client.patch(f"/order_lines/{order_line.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 5)

    def test_destroy_order_line_as_admin(self):
        """Test para eliminar una línea de pedido con un administrador"""
        order_line = OrderLine.objects.create(
            quantity=3,
            dish=self.dish,
            order=self.order,
            price=self.dish.price,
            total=self.dish.price * 3,
            subtotal=self.dish.price * 3,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.delete(f"/order_lines/{order_line.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class IncorrectOrderLineTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear un usuario administrador
        self.admin_user = User.objects.create_user(
            username="admin23",
            email="admin@example.com",
            password="admin123",
            is_staff=True,
            is_superuser=True,
            is_admin=True,
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        # Crear un restaurante, un plato y un pedido para pruebas
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.dish = Dish.objects.create(
            name="Pizza Margherita",
            description="Classic Italian pizza",
            price=9.99,
            dish_type="MAIN_COURSE",
            calories=20,
            preparation_time=20,
            ingredients=["Dough", "Tomato", "Mozzarella", "Basil"],
            is_active=True,
        )
        # Asegúrate de asignar un usuario al pedido
        self.order = Order.objects.create(
            restaurant=self.restaurant,
            total=100,
            total_dishes=10,
            status="PENDING",
            user=self.admin_user,
        )

        # Crear un usuario estándar
        self.standard_user = User.objects.create_user(
            username='standard',
            email='standard@example.com',
            password='standard123',
        )
        self.standard_token = Token.objects.create(user=self.standard_user)

    def test_create_order_line_with_invalid_data(self):
        """Probar creación de una línea de pedido con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            "quantity": 0,
            "dish": self.dish.pk,
            "order": self.order.pk,
            "price": -10,
        }

        response = self.client.post("/order_lines/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_line_as_standard_user(self):
        """Probar actualización de una línea de pedido con usuario estándar (debería fallar)"""
        order_line = OrderLine.objects.create(
            quantity=3,
            dish=self.dish,
            order=self.order,
            price=self.dish.price,
            total=self.dish.price * 3,
            subtotal=self.dish.price * 3,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {"quantity": 5}

        response = self.client.patch(f"/order_lines/{order_line.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_order_line_as_standard_user(self):
        """Probar eliminación de una línea de pedido con usuario estándar (debería fallar)"""
        order_line = OrderLine.objects.create(
            quantity=3,
            dish=self.dish,
            order=self.order,
            price=self.dish.price,
            total=self.dish.price * 3,
            subtotal=self.dish.price * 3,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        response = self.client.delete(f"/order_lines/{order_line.pk}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_non_existent_order_line(self):
        """Probar recuperación de una línea de pedido inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/order_lines/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)