from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from restaurants.models import Restaurant
from dishes.models import Dish
from restaurant_dish_link.models import RestaurantDishLink

class RestaurantDishLinkTests(TestCase):
    """Tests para el modelo RestaurantDishLink."""
    def setUp(self):
        """Configuración inicial de los tests."""
        self.client = APIClient()

        # Crear un usuario administrador con permisos
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

        # Crear un restaurante y un plato para usar en las pruebas
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

    def test_create_restaurant_dish_link_as_admin(self):
        """Test para crear un RestaurantDishLink con un administrador"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'restaurant': self.restaurant.pk,
            'dish': self.dish.pk,
            'stock': 10,
        }

        response = self.client.post("/restaurant_dish_link/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stock'], 10)

    def test_list_restaurant_dish_links(self):
        """Test para listar RestaurantDishLinks"""
        RestaurantDishLink.objects.create(
            restaurant=self.restaurant,
            dish=self.dish,
            stock=10,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/restaurant_dish_link/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_restaurant_dish_link(self):
        """Test para obtener detalles de un RestaurantDishLink"""
        restaurant_dish_link = RestaurantDishLink.objects.create(
            restaurant=self.restaurant,
            dish=self.dish,
            stock=10,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/restaurant_dish_link/{restaurant_dish_link.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock'], 10)

    def test_update_restaurant_dish_link_as_admin(self):
        """Test para actualizar un RestaurantDishLink con un administrador"""
        restaurant_dish_link = RestaurantDishLink.objects.create(
            restaurant=self.restaurant,
            dish=self.dish,
            stock=10,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {'stock': 20}

        response = self.client.patch(f"/restaurant_dish_link/{restaurant_dish_link.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock'], 20)

    def test_destroy_restaurant_dish_link_as_admin(self):
        """Test para eliminar un RestaurantDishLink con un administrador"""
        restaurant_dish_link = RestaurantDishLink.objects.create(
            restaurant=self.restaurant,
            dish=self.dish,
            stock=10,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.delete(f"/restaurant_dish_link/{restaurant_dish_link.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class IncorrectRestaurantDishLinkTests(TestCase):
    """Tests para el modelo RestaurantDishLink con datos incorrectos."""
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

        # Crear un restaurante y un plato para usar en las pruebas
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

    def test_create_restaurant_dish_link_as_standard_user(self):
        """Probar creación de un RestaurantDishLink con usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {
            'restaurant': self.restaurant.pk,
            'dish': self.dish.pk,
            'stock': 10,
        }

        response = self.client.post("/restaurant_dish_link/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_restaurant_dish_link_with_invalid_data(self):
        """Probar creación de un RestaurantDishLink con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        data = {
            'restaurant': self.restaurant.pk,
            'dish': self.dish.pk,
            'stock': -10,
        }

        response = self.client.post("/restaurant_dish_link/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_restaurant_dish_link_as_standard_user(self):
        """Probar actualización de un RestaurantDishLink con usuario estándar (debería fallar)"""
        restaurant_dish_link = RestaurantDishLink.objects.create(
            restaurant=self.restaurant,
            dish=self.dish,
            stock=10,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        data = {"stock": 20}

        response = self.client.patch(f"/restaurant_dish_link/{restaurant_dish_link.pk}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_restaurant_dish_link_as_standard_user(self):
        """Probar eliminación de un RestaurantDishLink con usuario estándar (debería fallar)"""
        restaurant_dish_link = RestaurantDishLink.objects.create(
            restaurant=self.restaurant,
            dish=self.dish,
            stock=10,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.standard_token.key)

        response = self.client.delete(f"/restaurant_dish_link/{restaurant_dish_link.pk}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_non_existent_restaurant_dish_link(self):
        """Probar recuperación de un RestaurantDishLink inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get("/restaurant_dish_link/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)