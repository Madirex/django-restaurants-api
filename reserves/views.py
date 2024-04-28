from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Reserve
from .serializers import ReserveSerializer
from users.permissions import IsAdminUser, IsStandardUser

class ReserveViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Un ViewSet para manejar las operaciones CRUD del modelo Reserve.
    """
    serializer_class = ReserveSerializer
    queryset = Reserve.objects.all()

    def get_permissions(self):
        """Determinar permisos basados en la acción"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStandardUser]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Crear una nueva reserva"""
        serializer = ReserveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserve = serializer.save()
        return Response(
            ReserveSerializer(reserve).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """Actualizar una reserva existente"""
        instance = self.get_object()
        serializer = ReserveSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            ReserveSerializer(instance).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """Eliminar una reserva"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
