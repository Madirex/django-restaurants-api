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
from django.utils.timezone import datetime
from reserves.models import Reserve
from orders.models import Order
from dishes.models import Dish
from restaurant_dish_link.models import RestaurantDishLink

class RestaurantTests(TestCase):
    """Tests para el modelo Restaurant."""
    def setUp(self):
        """Configuración inicial de los tests."""
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
    """Tests para el modelo Restaurant con datos incorrectos."""
    def setUp(self):
        """Configuración inicial de los tests."""
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

class RestaurantSchedulesTests(TestCase):
    """Tests para obtener horarios de un restaurante."""
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

        # Crear un calendario para usar en los tests
        self.calendar = Calendar.objects.create(
            normal_start_date=timezone.now(),
            summer_start_date=timezone.now() + timedelta(days=30),
            winter_start_date=timezone.now() + timedelta(days=60),
        )

        # Crear un restaurante con un calendario asignado
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            calendar=self.calendar,
        )

    def test_get_schedules_success(self):
        """Test para obtener horarios de un restaurante con fechas válidas"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        start_date = (datetime.now() + timedelta(days=1)).date().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=2)).date().strftime("%Y-%m-%d")

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/schedules/?start_date={start_date}&end_date={end_date}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_schedules_no_calendar(self):
        """Test para obtener horarios cuando no hay calendario asignado"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        # Crear un restaurante sin calendario
        restaurant_without_calendar = Restaurant.objects.create(name="No Calendar Restaurant")

        response = self.client.get(f"/restaurants/{restaurant_without_calendar.pk}/schedules/?start_date=2024-05-01&end_date=2024-05-02")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Este restaurante no tiene un calendario asignado.", response.data["error"])

    def test_get_schedules_missing_dates(self):
        """Test para obtener horarios sin proporcionar fechas"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/schedules/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Debes proporcionar 'start_date' y 'end_date'.", response.data["error"])

    def test_get_schedules_invalid_dates(self):
        """Test para obtener horarios con fechas en formato incorrecto"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/schedules/?start_date=invalid&end_date=also_invalid")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("El formato de fecha debe ser 'YYYY-MM-DD'.", response.data["error"])

    def test_get_schedules_start_after_end(self):
        """Test para obtener horarios con la fecha de inicio posterior a la fecha de finalización"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        start_date = "2024-05-03"
        end_date = "2024-05-01"

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/schedules/?start_date={start_date}&end_date={end_date}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("La fecha de inicio no puede ser posterior a la fecha de fin.", response.data["error"])

class RestaurantAvailableTablesTests(TestCase):
    """Tests para obtener mesas disponibles en un restaurante."""
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

        # Crear un calendario
        self.calendar = Calendar.objects.create(
            normal_start_date=timezone.now(),
            summer_start_date=timezone.now() + timedelta(days=30),
            winter_start_date=timezone.now() + timedelta(days=60),
        )

        # Crear un restaurante
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            calendar=self.calendar,
        )

        # Crear mesas para el restaurante
        self.table_1 = Table.objects.create(
            x_position=1,
            y_position=1,
            min_chairs=2,
            max_chairs=4,
            assigned_restaurant=self.restaurant,
        )

        self.table_2 = Table.objects.create(
            x_position=2,
            y_position=2,
            min_chairs=2,
            max_chairs=4,
            assigned_restaurant=self.restaurant,
        )

        # Crear order
        self.order = Order.objects.create(
            restaurant=self.restaurant,
            user=self.admin_user,
            total=100,
            total_dishes=10,
            status="PENDING",
        )

        # Crear reservas para las mesas
        now = timezone.now()
        self.reserve_1 = Reserve.objects.create(
            start_reserve=now + timedelta(days=1, hours=1),
            finish_reserve=now + timedelta(days=1, hours=3),
            assigned_order=self.order,
            assigned_chairs=2,
            table=self.table_1,
        )

    def test_get_available_tables_no_calendar(self):
        """Test para obtener mesas cuando el restaurante no tiene un calendario"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        # Crear un restaurante sin calendario
        restaurant_without_calendar = Restaurant.objects.create(name="No Calendar Restaurant")

        response = self.client.get(f"/restaurants/{restaurant_without_calendar.pk}/available-tables/?day=2024-05-01")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Este restaurante no tiene un calendario asignado.", response.data["error"])

    def test_get_available_tables_missing_day(self):
        """Test para obtener mesas sin proporcionar 'day'"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/available-tables/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Debe proporcionar el parámetro 'day' en formato 'YYYY-MM-DD'.", response.data["error"])

    def test_get_available_tables_invalid_day(self):
        """Test para obtener mesas con un parámetro 'day' en formato incorrecto"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/available-tables/?day=invalid-day")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Formato de fecha inválido. Use 'YYYY-MM-DD'.", response.data["error"])

    def test_get_available_tables_no_schedule(self):
        """Test para obtener mesas cuando no hay un Schedule para el día especificado"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        invalid_day = (datetime.now() - timedelta(days=10)).date().strftime("%Y-%m-%d")

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/available-tables/?day={invalid_day}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RestaurantMenuTests(TestCase):
    """Tests para obtener el menú de un restaurante"""
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

        # Crear un calendario
        self.calendar = Calendar.objects.create(
            normal_start_date=timezone.now(),
            summer_start_date=timezone.now() + timedelta(days=30),
            winter_start_date=timezone.now() + timedelta(days=60),
        )

        # Crear un restaurante
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            calendar=self.calendar,
        )

        # Crear platos
        self.dish1 = Dish.objects.create(name='Dish 1', description='Description 1', price=10.0, calories=100, preparation_time=20)
        self.dish2 = Dish.objects.create(name='Dish 2', description='Description 2', price=15.0, calories=150, preparation_time=25)

        # Crear enlaces entre restaurante y platos
        self.link1 = RestaurantDishLink.objects.create(restaurant=self.restaurant, dish=self.dish1, stock=10)
        self.link2 = RestaurantDishLink.objects.create(restaurant=self.restaurant, dish=self.dish2, stock=15)

    def test_get_menu(self):
        """Test para obtener el menú de un restaurante"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/restaurants/{self.restaurant.pk}/menu/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
