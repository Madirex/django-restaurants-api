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
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from schedules.models import Schedule

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Solo los administradores pueden realizar operaciones CRUD en los restaurantes

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'open_hours', 'get_schedules']:
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

    @action(detail=True, methods=['get'], url_path='schedules')
    def get_schedules(self, request, pk=None):
        restaurant = self.get_object()
        calendar = restaurant.calendar

        if calendar is None:
            return Response(
                {"error": "Este restaurante no tiene un calendario asignado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Obtener los parámetros de fechas desde la URL
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # Validación de las fechas
        if not start_date_str or not end_date_str:
            return Response(
                {"error": "Debes proporcionar 'start_date' y 'end_date'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "El formato de fecha debe ser 'YYYY-MM-DD'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start_date > end_date:
            return Response(
                {"error": "La fecha de inicio no puede ser posterior a la fecha de fin."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = []
        current_date = start_date

        while current_date <= end_date:
            custom_schedule = Schedule.objects.filter(calendar=calendar, day=current_date).first()

            if custom_schedule:
                response_data.append({
                    "date": str(current_date),
                    "schedule": [str(t) for t in custom_schedule.opened_hours],
                })
            elif current_date in calendar.closed_days:
                response_data.append({
                    "date": str(current_date),
                    "schedule": "Cerrado",
                })
            else:
                # Determinar la estación actual
                if calendar.normal_start_date <= current_date < calendar.summer_start_date:
                    schedule = calendar.normal_week_schedule
                elif calendar.summer_start_date <= current_date < calendar.winter_start_date:
                    schedule = calendar.summer_week_schedule
                else:
                    schedule = calendar.winter_week_schedule

                if schedule:
                    response_data.append({
                        "date": str(current_date),
                        "schedule": [str(t) for t in schedule.opened_hours],
                    })
                else:
                    response_data.append({
                        "date": str(current_date),
                        "schedule": "No hay horario disponible",
                    })

            current_date += timedelta(days=1)

        return Response(response_data, status=status.HTTP_200_OK)