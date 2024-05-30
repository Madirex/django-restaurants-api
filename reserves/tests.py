from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from orders.models import Order
from restaurants.models import Restaurant
from tables.models import Table
from reserves.models import Reserve
from django.utils import timezone
from datetime import timedelta

class ReserveTests(TestCase):
    """Tests para el modelo Reserve."""
    def setUp(self):
        """Configuración inicial de los tests."""
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

        # Crear restaurante y mesa
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.table = Table.objects.create(
            x_position=1,
            y_position=1,
            min_chairs=2,
            max_chairs=4,
            assigned_restaurant=self.restaurant,
            is_active=True,
        )

        # Crear orden para asignar a la reserva
        self.order = Order.objects.create(
            restaurant=self.restaurant,
            user=self.admin_user,
            total=100,
            total_dishes=10,
            status="PENDING",
        )

    def test_create_reserve_as_admin(self):
        """Test para crear una reserva como administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        now = timezone.now()
        data = {
            'start_reserve': now + timedelta(days=1),
            'finish_reserve': now + timedelta(days=1, hours=2),
            'assigned_order': self.order.pk,
            'assigned_chairs': 2,
            'table': self.table.pk,
        }

        response = self.client.post("/reserves/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['assigned_chairs'], 2)

    def test_list_reserves(self):
        """Test para listar reservas"""
        now = timezone.now()
        Reserve.objects.create(
            start_reserve=now + timedelta(days=1),
            finish_reserve=now + timedelta(days=1, hours=2),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/reserves/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_reserve(self):
        """Test para obtener detalles de una reserva"""
        now = timezone.now()
        reserve = Reserve.objects.create(
            start_reserve=now + timedelta(days=1),
            finish_reserve=now + timedelta(days=1, hours=2),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/reserves/{reserve.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['assigned_chairs'], 2)

    def test_update_reserve_as_admin(self):
        """Test para actualizar una reserva como administrador"""
        now = timezone.now()
        reserve = Reserve.objects.create(
            start_reserve=now + timedelta(days=1),
            finish_reserve=now + timedelta(days=1, hours=2),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {'assigned_chairs': 3, 'table': self.table.pk,'start_reserve': now + timedelta(days=1, hours=1),
         'finish_reserve': now + timedelta(days=1, hours=3)}

        response = self.client.patch(f"/reserves/{reserve.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['assigned_chairs'], 3)

    def test_destroy_reserve_as_admin(self):
        """Test para eliminar una reserva como administrador"""
        now = timezone.now()
        reserve = Reserve.objects.create(
            start_reserve=now + timedelta(days=1),
            finish_reserve=now + timedelta(days=1, hours=2),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

class IncorrectReserveTests(TestCase):
    """Tests para el modelo Reserve con errores."""
    def setUp(self):
        """Configuración inicial de los tests."""
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

        # Crear restaurante y mesa
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.table = Table.objects.create(
            x_position=1,
            y_position=1,
            min_chairs=2,
            max_chairs=4,
            assigned_restaurant=self.restaurant,
            is_active=True,
        )

        # Crear orden para asignar a la reserva
        self.order = Order.objects.create(
            restaurant=self.restaurant,
            user=self.admin_user,
            total=100,
            total_dishes=10,
            status="PENDING",
        )

    def test_create_reserve_with_negative_assigned_chairs(self):
        """Probar crear una reserva con un número negativo de sillas asignadas (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        now = timezone.now()
        data = {
            'start_reserve': now + timedelta(days=1),
            'finish_reserve': now + timedelta(days=1, hours=2),
            'assigned_order': self.order.pk,
            'assigned_chairs': -1,
            'table': self.table.pk,
        }

        response = self.client.post("/reserves/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reserve_with_superposition(self):
        """Probar crear una reserva que se superpone con otra existente (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        now = timezone.now()
        Reserve.objects.create(
            start_reserve=now + timedelta(days=1),
            finish_reserve=now + timedelta(days=1, hours=2),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table,
        )

        data = {
            'start_reserve': now + timedelta(days=1, hours=1),
            'finish_reserve': now + timedelta(days=1, hours=3),
            'assigned_order': self.order.pk,
            'assigned_chairs': 2,
            'table': self.table.pk,
        }

        response = self.client.post("/reserves/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reserve_with_inverted_times(self):
        """Probar crear una reserva donde la hora de inicio es posterior a la de finalización"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        now = timezone.now()
        data = {
            'start_reserve': now + timedelta(days=1, hours=2),
            'finish_reserve': now + timedelta(days=1, hours=1),
            'assigned_order': self.order.pk,
            'assigned_chairs': 2,
            'table': self.table.pk,
        }

        response = self.client.post("/reserves/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_reserve_with_superposition(self):
        """Probar actualizar una reserva que se superpone con otra existente"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        now = timezone.now()
        reserve1 = Reserve.objects.create(
            start_reserve=now + timedelta(days=1),
            finish_reserve=now + timedelta(days=1, hours=2),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table,
        )

        reserve2 = Reserve.objects.create(
            start_reserve=now + timedelta(days=2),
            finish_reserve=now + timedelta(days=2, hours=3),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table,
        )

        data = {
            'start_reserve': now + timedelta(days=2, hours=1),
            'finish_reserve': now + timedelta(days=2, hours=3),
            'assigned_chairs': 2,
        }

        response = self.client.patch(f"/reserves/{reserve1.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)