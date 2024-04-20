from rest_framework import serializers
from .models import Table
from django.core.validators import MinValueValidator
from datetime import datetime

class TableModelSerializer(serializers.ModelSerializer):
    """Serializer para el modelo de Mesa"""

    class Meta:
        model = Table
        fields = (
            'pk',
            'x_position',
            'y_position',
            'min_chairs',
            'max_chairs',
            #TODO: 'assignedOrder',
            #TODO: 'assignedChairs',
            'reserved',
            'reserved_at',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

class TableSerializer(serializers.Serializer):
    x_position = serializers.IntegerField(validators=[MinValueValidator(1)])
    y_position = serializers.IntegerField(validators=[MinValueValidator(1)])
    min_chairs = serializers.IntegerField(validators=[MinValueValidator(0)])
    max_chairs = serializers.IntegerField(validators=[MinValueValidator(0)])

    def validate(self, data):
        """Asegurarse de que min_chairs sea menor o igual a max_chairs."""
        if data['min_chairs'] > data['max_chairs']:
            raise serializers.ValidationError(
                "El mínimo de sillas debe ser menor o igual al máximo de sillas."
            )
        return data

    def create(self, validated_data):
        return Table.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
