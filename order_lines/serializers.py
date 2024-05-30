from rest_framework import serializers
from .models import OrderLine
from dishes.models import Dish
from orders.models import Order
import uuid

class OrderLineSerializer(serializers.ModelSerializer):
    """Serializer para el modelo OrderLine."""

    dish_name = serializers.CharField(source='dish.name', read_only=True)

    class Meta:
        """Clase Meta."""
        model = OrderLine
        fields = (
            'id',
            'quantity',
            'dish',
            'dish_name',
            'order',
            'price',
            'total',
            'subtotal',
            'selected',
        )
        read_only_fields = ('total', 'subtotal')

    def validate_quantity(self, value):
        """Validar que la cantidad sea al menos 1."""
        if value < 1:
            raise serializers.ValidationError("La cantidad debe ser al menos 1.")
        return value

    def create(self, validated_data):
        """Crear un nuevo OrderLine."""
        return OrderLine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Actualizar un OrderLine existente."""
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.dish = validated_data.get('dish', instance.dish)
        instance.selected = validated_data.get('selected', instance.selected)

        # Calcular de nuevo total y subtotal al actualizar
        instance.total = instance.quantity * instance.price
        instance.subtotal = instance.total

        instance.save()
        return instance
