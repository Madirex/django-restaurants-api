from rest_framework import serializers
from .models import Order, OrderStatus
from restaurants.models import Restaurant
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

    def validate_status(self, value):
    # Validar el campo 'status' para asegurar que es uno de los valores permitidos
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

class UserMakeOrderSerializer(serializers.ModelSerializer):
# TODO: El usuario podrá insertar un Order que tendrá diferentes order_lines
    """Serializer para crear un Order."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = (
            'restaurant',
            'total',
            'total_dishes',
            'cart_code',
        )

    # TODO: Esto solo lo podría ejecutar el usuario autenticado
    def validate(self, data):
        """Validar que el usuario no tenga un order pendiente."""
        user = data['user'] # TODO: esto debería de ser el usuario autentificado ¿¿¿ user = User.objects.get(pk=user.pk)
        restaurant = data['restaurant']
        cart_code = data['cart_code']

        if not Restaurant.objects.filter(pk=restaurant.pk).exists():
            raise serializers.ValidationError("El restaurante no existe.")

        # TODO: agregar comprobación de TIENDA actualmente abierta (en horario válido y con mesa disponible)

        if Order.objects.filter(user=user, restaurant=restaurant, status=OrderStatus.PENDING).exists():
            raise serializers.ValidationError("Ya tienes un pedido pendiente en este restaurante.")

        #TODO: FIX if not CartCode.objects.filter(code=cart_code, is_active=True, available_uses>=1).exists():
        #    raise serializers.ValidationError("El código de carrito no es válido o ya ha expirado.")

            #TODO: agregar 'restaurant_name',
            #TODO: agregar 'user_name',
            #TODO: agregar 'total',
            #TODO: agregar 'total_dishes',
            #TODO: agregar 'status',
        #TODO: Faltaría insertarlo

        return data

    def create(self, validated_data):
        """Crear un nuevo Order."""
        return Order.objects.create(**validated_data)