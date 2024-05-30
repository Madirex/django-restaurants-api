from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStandardUser, IsAdminUser
from restaurant_dish_link.models import RestaurantDishLink
from restaurant_dish_link.serializers import RestaurantDishLinkSerializer

class RestaurantDishLinkViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = RestaurantDishLinkSerializer
    queryset = RestaurantDishLink.objects.all()
    permission_classes_by_action = {
        'list': [IsAuthenticated, IsAdminUser],
        'retrieve': [IsAuthenticated, IsAdminUser],
        'create': [IsAuthenticated, IsAdminUser],
        'update': [IsAuthenticated, IsAdminUser],
        'partial_update': [IsAuthenticated, IsAdminUser],
        'destroy': [IsAuthenticated, IsAdminUser]
    }
    """Enlace restaurante con plato ViewSet"""

    def get_permissions(self):
        """Determinar permisos basados en la acción"""
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [IsAuthenticated])]

    def create(self, request, *args, **kwargs):
        """Crear un nuevo enlace de restaurante con plato"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Actualizar un enlace de restaurante con plato"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Obtener detalles de un enlace de restaurante con plato"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Eliminar un enlace de restaurante con plato"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
