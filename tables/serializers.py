from rest_framework import serializers
from .models import Table
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from restaurants.models import Restaurant
from orders.models import Order
from reserves.serializers import ReserveSerializer
from django.core.exceptions import ValidationError

class TableModelSerializer(serializers.ModelSerializer):
    """Serializer para el modelo de Mesa"""

    #ver datos reserves con Serializer de Reserve
    reserves = ReserveSerializer(many=True, read_only=True)

    class Meta:
        """Meta options."""
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
    pk = serializers.IntegerField(read_only=True)
    x_position = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    y_position = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    min_chairs = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_chairs = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    assigned_restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    is_active = serializers.BooleanField(default=True, required=False)
    """Serializer para el modelo de Mesa."""
    def validate(self, data):
        """Asegurarse de que min_chairs sea menor o igual a max_chairs. Asegurarse de que no exista una mesa en la misma posición."""
        if data['min_chairs'] > data['max_chairs']:
           raise serializers.ValidationError(
               "El mínimo de sillas debe ser menor o igual al máximo de sillas."
           )
        # Validación para posiciones únicas
        x_pos = data.get('x_position')
        y_pos = data.get('y_position')
        assigned_restaurant = data.get('assigned_restaurant')

        if x_pos is not None and y_pos is not None and assigned_restaurant is not None:
           # Verificar si ya existe una mesa con las mismas coordenadas en el mismo restaurante
           table_exists = Table.objects.filter(x_position=x_pos, y_position=y_pos, assigned_restaurant=assigned_restaurant)

           # Si es una actualización, debemos excluir el propio objeto de la verificación de unicidad
           if self.instance:
               table_exists = table_exists.exclude(pk=self.instance.pk)

           if table_exists.exists():
               raise serializers.ValidationError("Una mesa con esta posición ya existe.")

        return data

    def create(self, validated_data):
        """Crear una nueva mesa."""
        return Table.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Actualizar una mesa."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
