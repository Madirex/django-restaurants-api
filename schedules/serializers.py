from rest_framework import serializers
from schedules.models import Schedule
from django.core.exceptions import ValidationError
from calendars.models import Calendar
from utils.validators import validate_half_hour, validate_unique_schedule_day

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
        """Meta options."""
        model = Schedule
        fields = (
            'pk',
            'day',
            'opened_hours',
            'calendar',
        )

    def validate(self, data):
        """Validar que no exista un Schedule con el mismo día en el mismo calendario"""
        calendar = data.get("calendar")

        if not calendar:
            raise ValidationError("El 'Calendar' no puede ser nulo.")

        day = data.get("day")
        instance_id = self.instance.id if self.instance else None
        schedule_queryset = calendar.customs_schedules
        validate_unique_schedule_day(schedule_queryset, day, instance_id)
        return data