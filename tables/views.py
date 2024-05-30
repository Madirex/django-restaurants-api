from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TableModelSerializer, TableSerializer
from .models import Table
from users.permissions import IsAdminUser, IsStandardUser

class TableViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    Un ViewSet para manejar las operaciones CRUD del modelo Mesa.
    """
    serializer_class = TableModelSerializer
    queryset = Table.objects.all()

    def get_permissions(self):
        """Permiso para este viewset."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStandardUser]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Crear una mesa."""
        serializer = TableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        table = serializer.save()
        return Response(
            TableModelSerializer(table).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """Actualizar una mesa."""
        instance = self.get_object()
        serializer = TableSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(TableModelSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        """Eliminar una mesa."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
