from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderLineSerializer
from .models import OrderLine
from users.permissions import IsStandardUser, IsAdminUser

class OrderLineViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet para manejar OrderLine con operaciones CRUD."""
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

    def get_permissions(self):
        """Define permisos de administrador."""
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Crea un nuevo OrderLine."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_line = serializer.save()
        data = self.get_serializer(order_line).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Actualiza un OrderLine existente."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        """Elimina un OrderLine."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """Lista todos los OrderLine."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
