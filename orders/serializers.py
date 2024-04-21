from rest_framework import serializers
from .models import Order
from restaurants.models import Restaurant
from tables.models import Table
from users.models import User
from cartcodes.models import CartCode

class OrderSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Order."""
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = (
            'pk',
            'restaurant',
            'restaurant_name',
            'user',
            'user_name',
            'total',
            'total_dishes',
            'is_deleted',
            'status',
            'cart_code',
            'created_at',
            'updated_at',
            'finished_at',
        )

        read_only_fields = ('total', 'total_dishes')

    def validate_total(self, value):
        """Validar que el total sea al menos 0."""
        if value < 0:
            raise serializers.ValidationError("El total debe ser al menos 0.")
        return value

    def validate_total_dishes(self, value):
        """Validar que el total de dishes sea al menos 0."""
        if value < 0:
            raise serializers.ValidationError("El total de dishes debe ser al menos 0.")
        return value

    def create(self, validated_data):
        """Crear un nuevo Order."""
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Actualizar un Order existente."""
        instance.total = validated_data.get("total", instance.total)
        instance.total_dishes = validated_data.get("total_dishes", instance.total_dishes)
        instance.is_deleted = validated_data.get("is_deleted", instance.is_deleted)
        instance.status = validated_data.get("status", instance.status)
        instance.cart_code = validated_data.get("cart_code", instance.cart_code)

        instance.save()
        return instance
