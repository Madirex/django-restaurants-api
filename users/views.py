from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import UserLoginSerializer, UserSignUpSerializer, UserModelSerializer, UserMeModelSerializer
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserAddressUpdateSerializer
from orders.serializers import OrderSerializer, UserMakeOrderSerializer
import itsdangerous

class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Devolver los datos del usuario autenticado."""
        user = request.user
        serializer = UserMeModelSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def orders(self, request):
        """Devolver los pedidos del usuario autenticado."""
        user = request.user
        orders = user.orders.all()
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    #TODO: arreglar e implementar email (problema dependencia con versión actual DJango)
    #@action(detail=False, methods=['post'])
    #def signup(self, request):
    #    """Registro de usuario."""
    #    serializer = UserSignUpSerializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    user = serializer.save()
#
    #    # Generar un token seguro
    #    serializer = itsdangerous.URLSafeSerializer(settings.SECRET_KEY, salt='account-confirmation')
    #    token = serializer.dumps({'user_id': user.id})
#
    #    # Guardar el token en el usuario
    #    user.confirmation_token = token
    #    user.save()
#
    #    # Enviar el correo de confirmación
    #    confirmation_url = f"http://localhost:8000/confirm/{token}"
    #    send_mail(
    #        'Confirma tu cuenta',
    #        f'Por favor, confirma tu cuenta haciendo clic en el siguiente enlace: {confirmation_url}',
    #        settings.DEFAULT_FROM_EMAIL,
    #        [user.email],
    #    )
#
    #    return Response(UserModelSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def modify(self, request):
        """Update user data."""
        user = request.user

        if not request.data:
            return Response({"detail": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserModelSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_address(self, request):
        """Update user address."""
        user = request.user

        serializer = UserAddressUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Realizar un pedido (orders) con sus diferentes order_lines
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def order(self, request):
        """Create an order."""
        user = request.user
        serializer = UserMakeOrderSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=user)
        data = UserMakeOrderSerializer(order).data
        return Response(data, status=status.HTTP_201_CREATED)

    #TODO: arreglar e implementar email (problema dependencia con versión actual DJango)
    #@action(detail=False, methods=['get'], url_path='confirm/(?P<token>.+)')
    #def confirm(self, request, token):
    #    """Confirma la cuenta del usuario."""
    #    serializer = itsdangerous.URLSafeSerializer(settings.SECRET_KEY, salt='account-confirmation')
    #    try:
    #        data = serializer.loads(token)
    #        user_id = data.get('user_id')
#
    #        user = User.objects.get(id=user_id)
    #        user.is_confirmed = True
    #        user.confirmation_token = None  # Limpiar el token
    #        user.save()
#
    #        return Response({'message': 'Cuenta confirmada con éxito'}, status=status.HTTP_200_OK)
    #    except (User.DoesNotExist, BadSignature):
    #        return Response({'message': 'Token inválido o usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
