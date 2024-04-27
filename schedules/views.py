from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStandardUser, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule
from .serializers import ScheduleSerializer
from django.shortcuts import get_object_or_404

class ScheduleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet para el modelo Schedule"""

    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsStandardUser()]
        else:
            return [IsAuthenticated(), IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = ScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        schedule = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ScheduleSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        schedule = serializer.save()
        return Response(ScheduleSerializer(schedule).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)