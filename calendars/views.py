from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStandardUser, IsAdminUser
from .serializers import CalendarModelSerializer, CalendarSerializer
from .models import Calendar
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class CalendarViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet para Calendars"""

    serializer_class = CalendarModelSerializer
    queryset = Calendar.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStandardUser]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = CalendarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        calendar = serializer.save()
        data = CalendarModelSerializer(calendar).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CalendarSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(CalendarModelSerializer(instance).data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CalendarModelSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)