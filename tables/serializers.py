from rest_framework import serializers
from .models import Table
from django.core.validators import MinValueValidator
from datetime import datetime
from restaurants.models import Restaurant
from orders.models import Order
from reserves.serializers import ReserveSerializer

class TableModelSerializer(serializers.ModelSerializer):
    """Serializer para el modelo de Mesa"""

    #ver datos reserves con Serializer de Reserve
    reserves = ReserveSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = (
            'pk',
            'x_position',
            'y_position',
            'min_chairs',
            'max_chairs',
            'assigned_restaurant',
            'reserves',
            'is_active',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

class TableSerializer(serializers.Serializer):
    x_position = serializers.IntegerField(validators=[MinValueValidator(1)])
    y_position = serializers.IntegerField(validators=[MinValueValidator(1)])
    min_chairs = serializers.IntegerField(validators=[MinValueValidator(0)])
    max_chairs = serializers.IntegerField(validators=[MinValueValidator(0)])
    assigned_restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    is_active = serializers.BooleanField(default=True)

    def validate(self, data):
        """Asegurarse de que min_chairs sea menor o igual a max_chairs."""
        if data['min_chairs'] > data['max_chairs']:
            raise serializers.ValidationError(
                "El mínimo de sillas debe ser menor o igual al máximo de sillas."
            )
        """Asegurarse de que no exista una mesa en la misma posición."""
        # Validación para posiciones únicas
        x_pos = data['x_position']
        y_pos = data['y_position']

        # Verificar si ya existe una mesa con las mismas coordenadas
        table_exists = Table.objects.filter(x_position=x_pos, y_position=y_pos)

        # Si es una actualización, debemos excluir el propio objeto de la verificación de unicidad
        if self.instance:
            table_exists = table_exists.exclude(pk=self.instance.pk)

        if table_exists.exists():
            raise serializers.ValidationError("Una mesa con esta posición ya existe.")

        return data

    def create(self, validated_data):
        return Table.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
