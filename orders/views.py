from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import OrderSerializer
from .models import Order
from users.permissions import IsStandardUser, IsAdminUser
from django.utils import timezone
from restaurants.models import Restaurant
from dishes.models import Dish
from cartcodes.models import CartCode
from orders.models import Order, OrderStatus
from order_lines.models import OrderLine
from decimal import Decimal
from reserves.models import Reserve
from reserves.serializers import ReserveSerializer

class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet para manejar las operaciones CRUD de Order."""

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        """Define permisos de administrador."""
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Crea un nuevo Order."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()  # Guardar el nuevo pedido
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Actualiza un Order existente."""
        partial = kwargs.pop("partial", False)  # Permitir actualizaciones parciales
        instance = self.get_object()  # Obtener el pedido a actualizar
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()  # Guardar cambios
        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        """Elimina un Order."""
        instance = self.get_object()  # Obtener el pedido a eliminar
        self.perform_destroy(instance)  # Realizar la eliminación
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """Lista todos los pedidos."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Obtiene un Order específico."""
        instance = self.get_object()  # Obtener el pedido específico
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="finish")
    def finish_order(self, request, pk=None):
        """Marcar un pedido como finalizado."""
        instance = self.get_object()  # Obtener el pedido
        instance.finished_at = timezone.now()  # Marcar la fecha de finalización
        instance.save()
        return Response(self.get_serializer(instance).data)