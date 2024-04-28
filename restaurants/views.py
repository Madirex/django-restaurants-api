from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant
from .serializers import RestaurantSerializer
from users.permissions import IsStandardUser, IsAdminUser
from rest_framework.decorators import action
from tables.models import Table
from tables.serializers import TableSerializer
from reserves.models import Reserve
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Solo los administradores pueden realizar operaciones CRUD en los restaurantes

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'open_hours']:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]  # Solo los administradores pueden realizar operaciones CRUD en los restaurantes
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
