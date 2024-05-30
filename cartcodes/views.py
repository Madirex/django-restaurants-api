from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import (IsStandardUser, IsAdminUser)
from cartcodes.serializers import CartCodeSerializer
from cartcodes.models import CartCode

class CartCodeViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CartCodeSerializer
    queryset = CartCode.objects.all()
    """ViewSet para CartCodes."""

    def get_permissions(self):
        """Asigna permisos basados en la acción."""
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Crea un nuevo código de carrito."""
        serializer = CartCodeSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        cart_code = serializer.save()
        data = CartCodeSerializer(cart_code).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Actualiza un código de carrito."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(CartCodeSerializer(instance).data)

    def retrieve(self, request, *args, **kwargs):
        """Devuelve un código de carrito."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Elimina un código de carrito."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
