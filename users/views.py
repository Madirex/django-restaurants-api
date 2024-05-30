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
from rest_framework.exceptions import ValidationError
from tables.models import Table

class UserViewSet(viewsets.GenericViewSet):
    """User view set."""
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
        orders = user.orders.all().order_by('-created_at')
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
    # NOTE: NO HACER CON PK PORQUE DA ERROR - CUIDADO CON TypeError: UserViewSet.order() got an unexpected keyword argument 'pk'
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
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def order(self, request):
        """Crear un pedido."""
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
          "cart_code": cart_code_obj.id if cart_code_obj else None,
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
        tables = data.get("tables", [])
        start_reserve_str = data.get("start_reserve")
        finish_reserve_str = data.get("finish_reserve")
        date_format = "%Y-%m-%d %H:%M:%S"

        try:
            start_reserve = datetime.strptime(start_reserve_str, date_format)
        except ValueError:
            return Response({"error": "Formato de fecha y hora de inicio de la reserva inválido. Use 'YYYY-MM-DD HH:MM:SS'."}, status=status.HTTP_400_BAD_REQUEST)

        if start_reserve < datetime.now():
          return Response({"error": "La fecha y hora de inicio de la reserva no puede ser menor a la fecha y hora actual"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            finish_reserve = datetime.strptime(finish_reserve_str, date_format)
        except ValueError:
            return Response({"error": "Formato de fecha y hora de fin de la reserva inválido. Use 'YYYY-MM-DD HH:MM:SS'."}, status=status.HTTP_400_BAD_REQUEST)

        reserve_day = start_reserve.date()

        try:
          restaurant = Restaurant.objects.get(id=order_data["restaurant"])
        except Restaurant.DoesNotExist:
          return Response({"error": "El restaurante no existe."}, status=status.HTTP_404_NOT_FOUND)

        calendar = restaurant.calendar

        try:
          schedule = get_schedule_for_day(calendar, reserve_day)
        except Exception as e:
          return Response({'error': f'Error al obtener el horario para el día especificado. El calendario no se ha terminado de configurar correctamente. {e}'}, status=status.HTTP_400_BAD_REQUEST)

        opening_hours = schedule.opened_hours
        all_tables = restaurant.tables.all()

        reservations_day = Reserve.objects.filter(
          start_reserve__date=reserve_day,
          table__in=all_tables
        ).exclude(assigned_order__status=OrderStatus.CANCELLED)

        occupied_hours_per_table = {
          table.id: get_occupied_hours(
              reservations_day.filter(table=table),
              opening_hours
          ) for table in all_tables
        }
        for table_id in tables:
          try:
              table = all_tables.get(id=table_id)
          except Table.DoesNotExist:
              # eliminar reservas anteriores
              order.delete()
              return Response({"error": f"La mesa con ID {table_id} no fue encontrada."}, status=status.HTTP_404_NOT_FOUND)
          reserve_data = {
              "start_reserve": start_reserve_str,
              "finish_reserve": finish_reserve_str,
              "table": table_id,
              "assigned_order": order.id,
              "assigned_chairs": table.max_chairs,
          }

          reserve_serializer = ReserveSerializer(data=reserve_data)
          if not reserve_serializer.is_valid():
              return Response(reserve_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

          reserve_serializer.save()

        # Calcular el total y el total_dishes
        order.total = sum([line.subtotal for line in order.order_lines.all()])
        order.total_dishes = sum([line.quantity for line in order.order_lines.all()])
        order.save()
        # Aplicar cupón
        if cart_code_obj:
          order_total = Decimal(order.total)
          if cart_code_obj.fixed_discount > 0:
              fixed_discount = Decimal(cart_code_obj.fixed_discount)
              order_total -= fixed_discount
          elif cart_code_obj.percent_discount > 0:
              percent_discount = Decimal(cart_code_obj.percent_discount) / Decimal(100)
              discount = order_total * percent_discount
              order_total -= discount
          else:
              return Response({"error": "Tipo de cupón no válido"}, status=status.HTTP_400_BAD_REQUEST)
          if order_total < 0:
              order_total = Decimal(0)
          order.total = order_total
          order.save()
          cart_code_obj.available_uses -= 1
          cart_code_obj.save()
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_order(self, request, pk=None):
        """Cancelar un pedido."""
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