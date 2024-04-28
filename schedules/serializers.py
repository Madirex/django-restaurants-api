from rest_framework import serializers
from schedules.models import Schedule
from django.core.exceptions import ValidationError
from calendars.models import Calendar
from utils.validators import validate_half_hour

class ScheduleSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Schedule"""

    calendar = serializers.PrimaryKeyRelatedField(
        queryset=Calendar.objects.all(),
        help_text="Calendario asociado"
    )

    opened_hours = serializers.ListField(
        child=serializers.TimeField(),
        allow_empty=True,
        help_text="Horas de apertura",
        validators=[validate_half_hour]
    )

    class Meta:
        model = Schedule
        fields = (
            'pk',
            'day',
            'opened_hours',
            'calendar',
        )