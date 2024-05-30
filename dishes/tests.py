from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User
from dishes.models import Dish
from categories.models import Category

class DishTests(TestCase):
    """Test para platos."""
    def setUp(self):
        """Configuración inicial"""
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

        # Crear una categoría para usar en los tests
        self.category = Category.objects.create(name='Italian Food')

    def test_create_dish_as_admin(self):
        """Test para crear un plato con un administrador"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        # Datos para crear un nuevo plato
        data = {
            'name': 'Pasta Carbonara',
            'description': 'Delicious Italian dish',
            'price': 12.99,
            'dish_type': 'MAIN_COURSE',
            'ingredients': ['Pasta', 'Cream', 'Bacon', 'Parmesan'],
            'calories': 500,
            'preparation_time': 30,
            'category': self.category.name,
            'is_active': True,
        }

    def test_list_dishes(self):
        """Test para listar platos"""
        Dish.objects.create(
            name='Pizza Margherita',
            description='Classic Italian pizza',
            price=9.99,
            dish_type='MAIN_COURSE',
            ingredients=['Dough', 'Tomato', 'Mozzarella', 'Basil'],
            calories=400,
            preparation_time=20,
            category='Italian Food',
            is_active=True,
        )

        Dish.objects.create(
            name='Chicken Curry',
            description='Spicy Indian dish',
            price=10.99,
            dish_type='MAIN_COURSE',
            ingredients=['Chicken', 'Curry', 'Onion', 'Garlic'],
            calories=600,
            preparation_time=35,
            category='Indian Food',
            is_active=True,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        response = self.client.get('/dishes/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_dish(self):
        """Test para obtener detalles de un plato"""
        dish = Dish.objects.create(
            name='Spaghetti Bolognese',
            description='Italian dish with meat sauce',
            price=10.99,
            dish_type='MAIN_COURSE',
            ingredients=['Pasta', 'Meat', 'Tomato', 'Onion'],
            calories=500,
            preparation_time=25,
            category='Italian Food',
            is_active=True,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        response = self.client.get(f'/dishes/{dish.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Spaghetti Bolognese')

    def test_update_dish_as_admin(self):
        """Test para actualizar un plato con un administrador"""
        dish = Dish.objects.create(
            name='Grilled Cheese',
            description='Cheese sandwich grilled',
            price=5.99,
            dish_type='MAIN_COURSE',
            ingredients=['Bread', 'Cheese', 'Butter'],
            calories=300,
            preparation_time=10,
            category='American Food',
            is_active=True,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        data = {'name': 'Grilled Cheese Sandwich'}

        response = self.client.patch(f'/dishes/{dish.pk}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Grilled Cheese Sandwich')

    def test_destroy_dish_as_admin(self):
        """Test para eliminar un plato con un administrador"""
        dish = Dish.objects.create(
            name='Caesar Salad',
            description='Classic Caesar Salad',
            price=7.99,
            dish_type='APPETIZER',
            ingredients=['Lettuce', 'Croutons', 'Parmesan'],
            calories=250,
            preparation_time=15,
            category='Salads',
            is_active=True,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        response = self.client.delete(f'/dishes/{dish.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class IncorrectDishTests(TestCase):
    """Test para platos incorrectos."""
    def setUp(self):
        """Configuración inicial"""
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

        # Crear una categoría para usar en los tests
        self.category = Category.objects.create(name='Italian Food')

    def test_create_dish_as_standard_user(self):
        """Probar creación de plato con usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        data = {
            'name': 'Unauthorized Dish',
            'description': 'Test Dish',
            'price': 12.99,
            'dish_type': 'MAIN_COURSE',
            'ingredients': ['Test Ingredient'],
            'calories': 500,
            'preparation_time': 30,
            'category': self.category.name,
            'is_active': True,
        }

        response = self.client.post('/dishes/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_dish_with_invalid_data(self):
        """Probar creación de plato con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        data = {
            'name': '',
            'description': 'Test Dish',
            'price': -1,
            'dish_type': 'UNKNOWN',
            'calories': -100,
            'preparation_time': -10,
            'category': 'Non-Existent',
        }

        response = self.client.post('/dishes/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_dish_as_standard_user(self):
        """Probar actualización de plato con usuario estándar (debería fallar)"""
        dish = Dish.objects.create(
            name='Original Dish',
            description='Test Dish',
            price=12.99,
            dish_type='MAIN_COURSE',
            ingredients=['Test Ingredient'],
            calories=500,
            preparation_time=30,
            category='Italian Food',
            is_active=True,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        data = {'name': 'Unauthorized Update'}

        response = self.client.patch(f'/dishes/{dish.pk}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_dish_as_standard_user(self):
        """Probar eliminación de plato con usuario estándar (debería fallar)"""
        dish = Dish.objects.create(
            name='Dish to Delete',
            description='Test Dish',
            price=12.99,
            dish_type='MAIN_COURSE',
            ingredients=['Test Ingredient'],
            calories=500,
            preparation_time=30,
            category='Italian Food',
            is_active=True,
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        response = self.client.delete(f'/dishes/{dish.pk}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_non_existent_dish(self):
        """Probar recuperación de plato inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        response = self.client.get('/dishes/999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)