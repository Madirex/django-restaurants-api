from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStandardUser, IsAdminUser
from .serializers import DishModelSerializer, DishSerializer
from .models import Dish
from rest_framework.views import APIView

class DishViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = DishModelSerializer
    queryset = Dish.objects.all()
    """ViewSet para Platos."""

    def get_permissions(self):
        """Asigna permisos basados en la acción."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStandardUser]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Crea un nuevo plato."""
        serializer = DishSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        dish = serializer.save()
        data = DishModelSerializer(dish).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Actualiza un plato."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        #ignorar el campo 'image' durante la actualización si es tipo texto
        if 'image' in request.data and isinstance(request.data['image'], str):
            request.data.pop('image', None)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(DishModelSerializer(instance).data)

    def retrieve(self, request, *args, **kwargs):
        """Devuelve un plato."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Elimina un plato."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DishImageUpdateAPIView(APIView):
    """Vista para actualizar la imagen de un plato."""
    def patch(self, request, pk):
        """Actualiza la imagen de un plato."""
        try:
            dish = Dish.objects.get(pk=pk)
        except Dish.DoesNotExist:
            return Response({"error": "Plato no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Ignorar el campo 'category' durante la actualización
        request.data.pop('category', None)

        serializer = DishImageUpdateSerializer(instance=dish, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)