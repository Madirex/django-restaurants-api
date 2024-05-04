from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from categories.models import Category
from rest_framework.authtoken.models import Token

class CategoryTests(TestCase):
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

    def test_create_category_as_admin(self):
        """Test para crear una categoría con un administrador"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        url = "/categories/"

        data = {
            'name': 'new category',
            'is_active': True,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'new category')

    def test_list_categories(self):
        """Test para listar categorías"""
        Category.objects.create(name='Category1', is_active=True)
        Category.objects.create(name='Category2', is_active=True)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = "/categories/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_category(self):
        """Test para obtener detalles de una categoría"""
        category = Category.objects.create(name='Category1', is_active=True)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = f"/categories/{category.pk}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Category1')

    def test_update_category_as_admin(self):
        """Test para actualizar una categoría con un administrador"""
        category = Category.objects.create(name='Category1', is_active=True)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        url = f"/categories/{category.pk}/"

        data = {'name': 'Updated Category'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Category')

    def test_destroy_category_as_admin(self):
        """Test para eliminar una categoría con un administrador"""
        category = Category.objects.create(name='Category1', is_active=True)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        url = f"/categories/{category.pk}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class IncorrectCategoryTests(TestCase):
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

    def test_create_category_as_standard_user(self):
        """Probar creación de categoría con usuario estándar (debería fallar)"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = "/categories/"

        data = {
            'name': 'Unauthorized Category',
            'is_active': True,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_with_invalid_data(self):
        """Probar creación de categoría con datos inválidos"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        url = "/categories/"

        data = {
            'name': 'a' * 256,
            'is_active': True,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_non_existent_category(self):
        """Probar recuperación de categoría inexistente"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = "/categories/999/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category_as_standard_user(self):
        """Probar actualización de categoría con usuario estándar (debería fallar)"""
        category = Category.objects.create(name='Category1', is_active=True)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = f"/categories/{category.pk}/"

        data = {'name': 'Unauthorized Update'}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_as_standard_user(self):
        """Probar eliminación de categoría con usuario estándar (debería fallar)"""
        category = Category.objects.create(name='Category1', is_active=True)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.standard_token.key)

        url = f"/categories/{category.pk}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)