from rest_framework import serializers
from schedules.models import Schedule
from django.core.exceptions import ValidationError
from calendars.models import Calendar

class ScheduleSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Schedule"""

    calendar = serializers.PrimaryKeyRelatedField(
        queryset=Calendar.objects.all(),
        help_text="Calendario asociado"
    )

    opened_hours = serializers.ListField(
        child=serializers.TimeField(),
        allow_empty=True,
        help_text="Horas de apertura"
    )

    closed_hours = serializers.ListField(
        child=serializers.TimeField(),
        allow_empty=True,
        help_text="Horas de cierre"
    )

    class Meta:
        model = Schedule
        fields = (
            'pk',
            'day',
            'opened_hours',
            'closed_hours',
            'calendar',
        )

    def validate(self, data):
        """Validar que el número de horas de apertura y cierre coincida y que las horas de apertura sean antes que las de cierre"""
        opened_hours = data.get('opened_hours', [])
        closed_hours = data.get('closed_hours', [])

        if len(opened_hours) != len(closed_hours):
            raise serializers.ValidationError("El número de horas de apertura debe coincidir con el de cierre.")

        for open_time, close_time in zip(opened_hours, closed_hours):
            if open_time >= close_time:
                raise serializers.ValidationError("Cada hora de apertura debe ser antes de la hora de cierre correspondiente.")

        return data
