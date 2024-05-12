# Django
from django.test import TestCase

# Python
from PIL import Image
import tempfile
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from users.models import User
from orders.models import Order, OrderStatus
from restaurants.models import Restaurant

from rest_framework.authtoken.models import Token


class UserTestCase(TestCase):
    def setUp(self):
        user = User(
            email='tests@madirex.com',
            first_name='Admin',
            last_name='Admin',
            username='admintest'
        )
        user.set_password('Admin123-')
        user.save()

        # Obtener el token del usuario
        self.token = Token.objects.create(user=user)

    def test_signup_user(self):
        """Check if we can create an user"""

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        client = APIClient()
        response = client.post(
                '/users/signup/', {
                'email': 'angel2@madirex.com',
                'password': 'User123-',
                'password_confirmation': 'User123-',
                'first_name': 'User',
                'last_name': '1 2',
                'phone': '676556776',
                'username': 'User2',
                'city': 'Madrid',
                'country': 'Spain',
                'photo': tmp_file,
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_login_user(self):
        client = APIClient()
        response = client.post(
                '/users/login/', {
                'email': 'tests@madirex.com',
                'password': 'Admin123-',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        result = json.loads(response.content)
        self.assertIn('access_token', result)

    def test_login_user_invalid_password(self):
        """Test login with an incorrect password"""
        client = APIClient()
        response = client.post(
            '/users/login/',
            {
                'email': 'tests@madirex.com',
                'password': 'WrongPassword123',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('non_field_errors', result)
        self.assertEqual(result['non_field_errors'], ["Las credenciales no son válidas"])

    def test_login_user_invalid_email(self):
        """Test login with a non-existent email"""
        client = APIClient()
        response = client.post(
            '/users/login/',
            {
                'email': 'nonexistent@madirex.com',
                'password': 'Admin123-',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('non_field_errors', result)
        self.assertEqual(result['non_field_errors'], ["Las credenciales no son válidas"])


    def test_me_authenticated(self):
        client = APIClient()
        user = User.objects.get(username='admintest')
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.get('/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result['username'], 'admintest')
        self.assertEqual(result['first_name'], 'Admin')
        self.assertEqual(result['last_name'], 'Admin')

    def test_me_unauthenticated(self):
        response = self.client.get('/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserSignUpFailTests(TestCase):
    def setUp(self):
        user = User(
            email='existing@madirex.com',
            first_name='Existing',
            last_name='User',
            username='existinguser'
        )
        user.set_password('Password123!')
        user.save()

    def test_signup_user_password_mismatch(self):
        """Prueba de registro con contraseñas que no coinciden"""
        client = APIClient()
        response = client.post(
            '/users/signup/',
            {
                'email': 'testuser@madirex.com',
                'password': 'Password123!',
                'password_confirmation': 'DifferentPassword123!',
                'first_name': 'Test',
                'last_name': 'User',
                'username': 'testuser123',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = json.loads(response.content)
        self.assertIn('non_field_errors', result)
        self.assertEqual(result['non_field_errors'], ["Las contraseñas no coinciden"])

    def test_signup_user_existing_email(self):
        """Prueba de registro con correo electrónico existente"""
        client = APIClient()
        response = client.post(
            '/users/signup/',
            {
                'email': 'existing@madirex.com',
                'password': 'Password123!',
                'password_confirmation': 'Password123!',
                'first_name': 'Test',
                'last_name': 'User',
                'username': 'testuser123',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = json.loads(response.content)
        self.assertIn('email', result)
        self.assertEqual(result['email'], ["Este campo debe ser único."])

    def test_signup_user_existing_username(self):
        """Prueba de registro con nombre de usuario existente"""
        client = APIClient()
        response = client.post(
            '/users/signup/',
            {
                'email': 'newuser@madirex.com',
                'password': 'Password123!',
                'password_confirmation': 'Password123!',
                'first_name': 'Test',
                'last_name': 'User',
                'username': 'existinguser',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = json.loads(response.content)
        self.assertIn('username', result)
        self.assertEqual(result['username'], ["Este campo debe ser único."])

    def test_signup_user_invalid_phone(self):
        """Prueba de registro con número de teléfono inválido"""
        client = APIClient()
        response = client.post(
            '/users/signup/',
            {
                'email': 'newuser@madirex.com',
                'password': 'Password123!',
                'password_confirmation': 'Password123!',
                'first_name': 'Test',
                'last_name': 'User',
                'username': 'testuser456',
                'phone': '12345',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = json.loads(response.content)
        self.assertIn('phone', result)
        self.assertEqual(result['phone'], ["Debes introducir un número con el siguiente formato: +999999999. El límite son de 15 dígitos."])

class UserModifyTests(TestCase):
    def setUp(self):
        self.user = User(
            email='modify@madirex.com',
            first_name='Mod',
            last_name='Ify',
            username='modifyuser'
        )
        self.user.set_password('Password123!')
        self.user.save()

        self.token = Token.objects.create(user=self.user)

        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_modify_user_success(self):
        """Test para modificar un usuario exitosamente"""
        response = self.auth_client.put(
            '/users/me/',
            {
                'first_name': 'Modified',
                'last_name': 'Name',
                'phone': '+123456789',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result['first_name'], 'Modified')
        self.assertEqual(result['last_name'], 'Name')
        self.assertEqual(result['phone'], '+123456789')

    def test_modify_user_unauthorized(self):
        """Test para modificar sin autenticación"""
        client = APIClient()
        response = client.put(
            '/users/me/',
            {
                'first_name': 'Unauthorized',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_user_duplicate_email(self):
        """Test para modificar con un correo electrónico duplicado"""
        User.objects.create(
            email='duplicate@madirex.com',
            first_name='Dupe',
            last_name='User',
            username='dupeuser',
            password='Password123!'
        )

        response = self.auth_client.put(
            '/users/me/',
            {
                'email': 'duplicate@madirex.com',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('email', result)
        self.assertEqual(result['email'], ["Ya existe usuario con este email address."])

    def test_modify_user_invalid_phone(self):
        """Test para modificar con un número de teléfono inválido"""
        response = self.auth_client.put(
            '/users/me/',
            {
                'phone': '12345',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('phone', result)
        self.assertEqual(result['phone'], ["Debes introducir un número con el siguiente formato: +999999999. El límite son de 15 dígitos."])

class UserModifyTests(TestCase):
    def setUp(self):
        self.user = User(
            email='modify@madirex.com',
            first_name='Mod',
            last_name='Ify',
            username='modifyuser'
        )
        self.user.set_password('Password123!')
        self.user.save()

        self.token = Token.objects.create(user=self.user)

        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_modify_user_success(self):
        """Test para modificar un usuario exitosamente"""
        response = self.auth_client.patch(
            '/users/modify/',
            {
                'first_name': 'Modified',
                'last_name': 'Name',
                'phone': '+123456789',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result['first_name'], 'Modified')
        self.assertEqual(result['last_name'], 'Name')
        self.assertEqual(result['phone'], '+123456789')

    def test_modify_user_unauthorized(self):
        """Test para modificar sin autenticación"""
        client = APIClient()
        response = client.patch(
            '/users/modify/',
            {
                'first_name': 'Unauthorized',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_user_duplicate_email(self):
        """Test para modificar con un correo electrónico duplicado"""
        User.objects.create(
            email='duplicate@madirex.com',
            first_name='Dupe',
            last_name='User',
            username='dupeuser',
            password='Password123!'
        )

        response = self.auth_client.patch(
            '/users/modify/',
            {
                'email': 'duplicate@madirex.com',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('email', result)
        self.assertEqual(result['email'], ["Ya existe usuario con este email address."])

class UserAddressUpdateTests(TestCase):
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User(
            email='user@madirex.com',
            first_name='Address',
            last_name='Tester',
            username='addresstester'
        )
        self.user.set_password('Password123!')
        self.user.save()

        # Crear un token para autenticación
        self.token = Token.objects.create(user=self.user)

        # Cliente autenticado
        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_address_success(self):
        """Test para actualizar la dirección con éxito"""
        response = self.auth_client.put(
            '/users/update_address/',
            {
                'address': {
                    'street': 'Calle Falsa',
                    'number': '123',
                    'city': 'Madrid',
                    'province': 'Madrid',
                    'country': 'Spain',
                    'postal_code': '28001',
                },
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertEqual(result['address']['street'], 'Calle Falsa')
        self.assertEqual(result['address']['number'], '123')
        self.assertEqual(result['address']['city'], 'Madrid')
        self.assertEqual(result['address']['province'], 'Madrid')
        self.assertEqual(result['address']['country'], 'Spain')
        self.assertEqual(result['address']['postal_code'], '28001')

    def test_update_address_unauthorized(self):
        """Test para actualizar sin autenticación"""
        client = APIClient()
        response = client.put(
            '/users/update_address/',
            {
                'address': {
                    'street': 'Unauthorized Street',
                    'city': 'Unauthorized City',
                },
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_address_invalid_json(self):
        """Test para actualizar con una dirección que no es un objeto JSON"""
        response = self.auth_client.put(
            '/users/update_address/',
            {
                'address': "Not a JSON object",
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('address', result)
        self.assertEqual(result['address'], ["La dirección debe ser un objeto JSON."])

    def test_update_address_with_unexpected_fields(self):
        """Test para actualizar con campos no permitidos"""
        response = self.auth_client.put(
            '/users/update_address/',
            {
                'address': {
                    'unexpected_field': 'Should not be here',
                },
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('address', result)
        self.assertEqual(result['address'], ["Los siguientes campos no están permitidos: unexpected_field"])

    def test_update_address_with_long_fields(self):
        """Test para actualizar con campos demasiado largos"""
        response = self.auth_client.put(
            '/users/update_address/',
            {
                'address': {
                    'street': 'A' * 150,
                },
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn('address', result)
        self.assertEqual(result['address'], ["El campo 'street' no debe exceder 100 caracteres."])

class OrderTests(TestCase):
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User(
            email='orders@madirex.com',
            first_name='Order',
            last_name='Tester',
            username='ordertester'
        )
        self.user.set_password('Password123!')
        self.user.save()

        # Crear un token para autenticación
        self.token = Token.objects.create(user=self.user)

        # Cliente autenticado
        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Crear un restaurante para las pruebas
        self.restaurant = Restaurant.objects.create(
            name='Restaurant Test',
            description='A restaurant for testing'
        )

        # Crear algunos pedidos para el usuario
        Order.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            total=100,
            total_dishes=5,
            status=OrderStatus.PENDING,
        )

        Order.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            total=200,
            total_dishes=10,
            status=OrderStatus.DELIVERED,
        )

    def test_get_orders_success(self):
        """Test para obtener pedidos exitosamente"""
        response = self.auth_client.get(
            '/orders/',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertTrue(len(result) >= 2)

    def test_get_orders_unauthorized(self):
        """Test para obtener pedidos sin autenticación"""
        client = APIClient()
        response = client.get(
            '/orders/',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_check_fields(self):
        """Test para verificar los campos de los pedidos"""
        response = self.auth_client.get(
            '/orders/',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)

        # Verificar que el primer pedido tenga los campos correctos
        first_order = result[0]
        self.assertIn('restaurant_name', first_order)
        self.assertIn('user_name', first_order)
        self.assertIn('total', first_order)
        self.assertIn('total_dishes', first_order)
        self.assertIn('status', first_order)

    def test_get_orders_check_pagination(self):
        """Test para verificar paginación"""
        response = self.auth_client.get(
            '/orders/',  # Endpoint para obtener pedidos
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('results', json.loads(response.content))

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crea un usuario para las pruebas
        self.user = User.objects.create_user(
            email='user1@madirex.com',
            first_name='User',
            last_name='One',
            username='userone',
            password='Password123!'
        )

        self.token = Token.objects.create(user=self.user)

        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            total=100,
            total_dishes=5,
        )

    def test_get_orders_unauthorized(self):
        """Test para obtener pedidos sin autenticación"""
        client = APIClient()
        response = client.get('/orders/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GetOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuario y pedido
        self.user = User.objects.create_user(
            username='ordertester',
            email='orders@madirex.com',
            password='Password123!',
        )
        self.token = Token.objects.create(user=self.user)
        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Crear restaurante y pedido
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        self.order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            total=100,
            total_dishes=5,
        )

    def test_get_order_success(self):
        """Test para obtener un pedido específico del usuario autenticado"""
        response = self.auth_client.get(
            f'/users/get_order/?order_id={self.order.id}',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['total'], '100.00')

    def test_get_order_not_found(self):
        """Test para obtener un pedido inexistente"""
        response = self.auth_client.get(
            '/users/get_order/?order_id=99999',  # ID inexistente
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content)['error'], "Pedido no encontrado.")

class GetOrderByPkTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='ordertester',
            email='orders@madirex.com',
            password='Password123!',
        )
        self.token = Token.objects.create(user=self.user)
        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Crear restaurante y pedido
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        self.order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            total=100,
            total_dishes=5,
        )

    def test_order_get_by_pk_not_found(self):
        """Test para obtener un pedido con pk inexistente"""
        response = self.auth_client.get(
            '/users/order/99999/',  # ID inexistente
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CancelOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='ordertester',
            email='orders@madirex.com',
            password='Password123!',
        )
        self.token = Token.objects.create(user=self.user)
        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        self.order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            total=100,
            total_dishes=5,
        )

    def test_cancel_order_success(self):
        """Test para cancelar un pedido exitosamente"""
        response = self.auth_client.post(
            f'/users/cancel_order/{self.order.id}/',
            {},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', json.loads(response.content))
        self.assertEqual(json.loads(response.content)['message'], "Pedido cancelado exitosamente.")

    def test_cancel_order_not_found(self):
        """Test para cancelar un pedido inexistente"""
        response = self.auth_client.post(
            '/users/cancel_order/99999/',  # Pedido inexistente
            {},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', json.loads(response.content))
        self.assertEqual(json.loads(response.content)['error'], "Pedido no encontrado.")

    def test_cancel_order_already_cancelled(self):
        """Test para cancelar un pedido que ya fue cancelado"""
        self.order.status = OrderStatus.CANCELLED
        self.order.save()

        response = self.auth_client.post(
            f'/users/cancel_order/{self.order.id}/',
            {},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', json.loads(response.content))
        self.assertEqual(json.loads(response.content)['error'], "El pedido ya está cancelado.")
