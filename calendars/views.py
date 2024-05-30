from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStandardUser, IsAdminUser
from .serializers import CalendarModelSerializer, CalendarSerializer
from .models import Calendar
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from datetime import datetime, date

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
        """Asigna permisos basados en la acción."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStandardUser]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Crea un nuevo calendario."""
        serializer = CalendarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        calendar = serializer.save()
        data = CalendarModelSerializer(calendar).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Actualiza un calendario."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CalendarSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(CalendarModelSerializer(instance).data)

    def retrieve(self, request, *args, **kwargs):
        """Devuelve un calendario."""
        instance = self.get_object()
        serializer = CalendarModelSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Elimina un calendario."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['post'], url_path='add-closed-day')
    def add_closed_day(self, request, pk=None):
        """Agrega un día de cierre al calendario."""
        calendar = self.get_object()
        closed_day_str = request.data.get('closed_day')
        if not closed_day_str:
            return Response({'detail': 'El día de cierre no se ha proporcionado.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            closed_day = datetime.strptime(closed_day_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'Formato de fecha inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        if closed_day in calendar.closed_days:
            return Response({'detail': 'El día de cierre ya está agregado en la lista.'}, status=status.HTTP_400_BAD_REQUEST)

        if closed_day < date.today():
            return Response({'detail': 'El día de cierre debe ser hoy o una fecha futura.'}, status=status.HTTP_400_BAD_REQUEST)

        calendar.closed_days.append(closed_day)
        calendar.save()
        return Response(CalendarModelSerializer(calendar).data)

    @action(detail=True, methods=['delete'], url_path='remove-closed-day')
    def remove_closed_day(self, request, pk=None):
        """Elimina un día de cierre del calendario."""
        calendar = self.get_object()
        closed_day_str = request.data.get('closed_day')
        if not closed_day_str:
            return Response({'detail': 'Día de cierre no proporcionado.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            closed_day = datetime.strptime(closed_day_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'Formato de fecha inválido. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        if closed_day not in calendar.closed_days:
            return Response({'detail': 'Día de cierre no se encuentra agregado.'}, status=status.HTTP_400_BAD_REQUEST)

        calendar.closed_days.remove(closed_day)
        calendar.save()
        return Response(CalendarModelSerializer(calendar).data, status=status.HTTP_200_OK)