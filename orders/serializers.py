from rest_framework import serializers
from .models import Order, OrderStatus
from restaurants.models import Restaurant
from users.models import User
from cartcodes.models import CartCode
from order_lines.serializers import OrderLineSerializer
from reserves.serializers import ReserveSerializer
from reserves.models import Reserve
from datetime import timedelta

class OrderSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Order."""
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    order_lines = OrderLineSerializer(many=True, read_only=True)
    reserves = ReserveSerializer(many=True, read_only=True)

    class Meta:
        """Clase Meta."""
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
            'order_lines',
            'reserves',
            'created_at',
            'updated_at',
            'finished_at',
        )

        read_only_fields = ('total', 'total_dishes')

    def validate_status(self, value):
        """Validar que el estado sea uno de los valores permitidos."""
        if value not in [choice.value for choice in OrderStatus]:
            raise serializers.ValidationError({
                "status": f"Estado no válido: {value}. Debe ser uno de los valores permitidos: {', '.join([choice.value for choice in OrderStatus])}."
            })
        return value

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

    def validate_restaurant(self, value):
        """Validar que el restaurante exista."""
        if not Restaurant.objects.filter(name=value).exists():
            raise serializers.ValidationError("El restaurante especificado no existe.")
        return value

    def create(self, validated_data):
        """Crear un nuevo Order."""
        validated_data['status'] = OrderStatus.PENDING
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