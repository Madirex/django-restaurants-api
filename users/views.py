from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import UserLoginSerializer, UserSignUpSerializer, UserModelSerializer, UserMeModelSerializer
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserAddressUpdateSerializer
from orders.serializers import OrderSerializer
import itsdangerous
from orders.models import Order, OrderStatus
from dishes.models import Dish
from order_lines.models import OrderLine
from decimal import Decimal
from reserves.serializers import ReserveSerializer
from cartcodes.models import CartCode
from datetime import datetime
from restaurants.models import Restaurant
from utils.calendar_utils import get_schedule_for_day, get_occupied_hours, get_available_hours
from reserves.models import Reserve

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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_order(self, request):
        """Devolver un pedido específico del usuario autenticado."""
        order_id = request.query_params.get('order_id', None)

        if not order_id:
            return Response({"error": "El pedido (order_id) no se ha proporcionado."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(id=order_id, user=request.user).first()

        if not order:
            return Response({"error": "Pedido no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Acción para obtener un pedido por ID
    #NO HACER CON PK PORQUE DA ERROR - CUIDADO CON TypeError: UserViewSet.order() got an unexpected keyword argument 'pk'
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def order(self, request, pk=None):
        """Devolver un pedido específico del usuario autenticado."""
        order = Order.objects.filter(id=pk, user=request.user).first()
        if not order:
            return Response({"error": "Pedido no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
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
    # Crear Order y realizar operaciones
        data = request.data

        cart_code_code = data.get("cart_code_code")
        cart_code_obj = None

        if cart_code_code:
            cart_code_obj = CartCode.objects.filter(code=cart_code_code).first()
            if not cart_code_obj:
                return Response({"error": "El código de carrito no es válido."}, status=status.HTTP_400_BAD_REQUEST)
            elif cart_code_obj.available_uses < 1:
                return Response({"error": "El código de carrito no tiene usos disponibles."}, status=status.HTTP_400_BAD_REQUEST)

        # Datos del pedido
        order_data = {
            "restaurant": data.get("restaurant"),
            "user": request.user.id,
            "total": Decimal(data.get("total", 0)),
            "total_dishes": data.get("total_dishes", 0),
            "cart_code": data.get("cart_code", cart_code_obj.id if cart_code_obj else None),
            "status": OrderStatus.PENDING
        }

        # Crear el pedido
        order_serializer = OrderSerializer(data=order_data)
        if not order_serializer.is_valid():
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = order_serializer.save()

        # Crear las líneas de pedido
        order_lines = data.get("order_lines", [])
        for line in order_lines:
            dish_id = line.get("dish")
            quantity = line.get("quantity", 1)

            dish = Dish.objects.filter(id=dish_id).first()
            if not dish:
                return Response({"error": f"El plato con ID {dish_id} no fue encontrado."}, status=status.HTTP_404_NOT_FOUND)

            price = dish.price
            subtotal = price * quantity

            OrderLine.objects.create(
                order=order,
                quantity=quantity,
                dish=dish,
                price=price,
                subtotal=subtotal,
                total=subtotal
            )

        # Crear la reserva asociada al pedido
        reserve_data = {
            "start_reserve": data.get("start_reserve"),
            "finish_reserve": data.get("finish_reserve"),
            "table": data.get("table"),
            "assigned_order": order.id,
            "assigned_chairs": data.get("assigned_chairs", 1),
        }

        # start reserve no puede ser menor al día y hora de hoy
        # Define el formato en que llega la fecha como cadena
        date_format = "%Y-%m-%d %H:%M:%S"

        # Convierte el string a datetime antes de la comparación
        start_reserve = datetime.strptime(reserve_data["start_reserve"], date_format)

        # Ahora compara
        if start_reserve < datetime.now():
            return Response({"error": "La fecha y hora de inicio de la reserva no puede ser menor a la fecha y hora actual"}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir a datetime
        start_reserve = datetime.strptime(reserve_data["start_reserve"], "%Y-%m-%d %H:%M:%S")
        finish_reserve = datetime.strptime(reserve_data["finish_reserve"], "%Y-%m-%d %H:%M:%S")

        # Obtener el día de la reserva
        reserve_day = start_reserve.date()

        # Obtener el restaurante y su calendario
        restaurant = Restaurant.objects.get(id=order_data["restaurant"])
        calendar = restaurant.calendar

        # Obtener el schedule para el día especificado
        schedule = get_schedule_for_day(calendar, reserve_day)

        # Obtener las horas de apertura
        opening_hours = schedule.opened_hours

        # Obtener todas las mesas del restaurante
        tables = restaurant.tables.all()

        # Obtener reservas para ese día y mesa
        reservations_day = Reserve.objects.filter(
            start_reserve__date=reserve_day,
            table__in=tables
        ).exclude(assigned_order__status=OrderStatus.CANCELLED)

        # Calcular las horas ocupadas para la mesa específica
        occupied_hours = get_occupied_hours(
            reservations_day.filter(table=reserve_data["table"]),
            opening_hours
        )

        # Calcular las horas disponibles para esa mesa
        available_hours = get_available_hours(opening_hours, occupied_hours)

        # Verificar si el intervalo de reserva está dentro de las horas disponibles
        # Calcular las horas disponibles para cada mesa
        response_data = []
        occupied_hours_per_table = {
            table.id: get_occupied_hours(
                reservations_day.filter(table=table),
                opening_hours
            ) for table in tables
        }
        for table in tables:
            available_hours = get_available_hours(
                opening_hours,
                occupied_hours_per_table[table.id]
            )

            # Crear la estructura para cada mesa con detalles y horas disponibles
            response_data.append({
                "table": table.id,
                "available_hours": available_hours
            })

        reserve_serializer = ReserveSerializer(data=reserve_data)
        if not reserve_serializer.is_valid():
            return Response(reserve_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        reserve_serializer.save()

        # Ahora calcular el total y el total_dishes
        order.total = sum([line.subtotal for line in order.order_lines.all()])
        order.total_dishes = sum([line.quantity for line in order.order_lines.all()])
        order.save()

        # Ahora aplicar cupón (comprobar si es válido y si tipo fixed o no) y aplicar descuento correspondiente
        # Asegúrate de que el total del pedido es Decimal
        order_total = Decimal(order.total)

        # Comprobar si el descuento es fijo
        if cart_code_obj:
            if cart_code_obj.fixed_discount > 0:
                fixed_discount = Decimal(cart_code_obj.fixed_discount)
                order_total -= fixed_discount

            # Comprobar si el descuento es por porcentaje
            elif cart_code_obj.percent_discount > 0:
                # Convertir el porcentaje a Decimal antes de aplicar
                percent_discount = Decimal(cart_code_obj.percent_discount) / Decimal(100)
                discount = order_total * percent_discount
                order_total -= discount
            # Si no hay un descuento válido
            else:
                return Response({"error": "Tipo de cupón no válido"}, status=status.HTTP_400_BAD_REQUEST)

            if order_total < 0:
                order_total = Decimal(0)
            # Guardar el total modificado
            order.total = order_total  # Reasignar el total corregido
            order.save()
            cart_code_obj.available_uses -= 1
            cart_code_obj.save()


        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_order(self, request, pk=None):
        # Obten el pedido por ID y verifica que pertenece al usuario autenticado
        order = Order.objects.filter(id=pk, user=request.user).first()

        # Si no se encuentra
        if not order:
            return Response({"error": "Pedido no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si ya está cancelado
        if order.status == OrderStatus.CANCELLED:
            return Response({"error": "El pedido ya está cancelado."}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar el estado a CANCELLED
        order.status = OrderStatus.CANCELLED
        order.save()

        # Si hay cupón asociado, aumentar sus usos disponibles
        if order.cart_code:
            order.cart_code.available_uses += 1
            order.cart_code.save()

        return Response({"message": "Pedido cancelado exitosamente."}, status=status.HTTP_200_OK)

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
