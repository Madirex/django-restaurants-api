from rest_framework import serializers
from .models import Calendar
from schedules.models import Schedule
from django.core.validators import MinValueValidator

class ScheduleModelSerializer(serializers.ModelSerializer):
    """Schedule Model Serializer"""

    class Meta:
        model = Schedule
        fields = ('pk', 'day', 'opened_hours', 'closed_hours')

class CalendarModelSerializer(serializers.ModelSerializer):
    """Calendar Model Serializer"""

    schedules = ScheduleModelSerializer(many=True, read_only=True)  # Incluir los Schedules asociados

    class Meta:
        model = Calendar
        fields = (
            'pk',
            'normal_week_schedule',
            'summer_week_schedule',
            'winter_week_schedule',
            'normal_start_date',
            'summer_start_date',
            'winter_start_date',
            'closed_days',
            'schedules',  # Incluir el campo schedules
        )

class CalendarSerializer(serializers.Serializer):
    """Serializer para crear/actualizar Calendarios"""

    normal_week_schedule = serializers.DateField()
    summer_week_schedule = serializers.DateField(required=False)
    winter_week_schedule = serializers.DateField(required=False)
    normal_start_date = serializers.DateField()
    summer_start_date = serializers.DateField(required=False)
    winter_start_date = serializers.DateField(required=False)
    closed_days = serializers.ListField(
        child=serializers.DateField(),
        allow_empty=True,
        default=list,
        help_text="Lista de días cerrados"
    )

    def create(self, validated_data):
        calendar = Calendar.objects.create(**validated_data)
        return calendar

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
