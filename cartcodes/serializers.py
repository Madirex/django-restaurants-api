# Django REST Framework
from rest_framework import serializers
# Model
from cartcodes.models import CartCode

class CartCodeModelSerializer(serializers.ModelSerializer):
    """CartCode Model Serializer"""

    class Meta:
        """Meta class."""

        model = CartCode
        fields = (
            'code',
            'is_active',
            'percent_discount',
            'fixed_discount',
            'available_uses',
            'expiration_date',
        )

class CartCodeSerializer(serializers.Serializer):
    """Serializer para crear/actualizar códigos de carrito"""
    id = serializers.UUIDField(read_only=True)
    code = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True, required=False)
    percent_discount = serializers.FloatField(min_value=0, max_value=100)
    fixed_discount = serializers.FloatField()
    available_uses = serializers.IntegerField()
    expiration_date = serializers.DateTimeField(required=False, allow_null=True)


    def validate_code(self, value):
        """
        Check if the code is unique, except if it's the same as the current instance.
        """
        if self.instance and self.instance.code == value:
            return value
        if CartCode.objects.filter(code=value).exists():
            raise serializers.ValidationError('El código ya existe.')
        return value


    def update(self, instance, validated_data):
        """Actualiza un código de carrito."""
        instance.code = validated_data.get('code', instance.code)
        if CartCode.objects.exclude(pk=instance.pk).filter(code=instance.code).exists():
            raise serializers.ValidationError("This code already exists.")
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.percent_discount = validated_data.get('percent_discount', instance.percent_discount)
        instance.fixed_discount = validated_data.get('fixed_discount', instance.fixed_discount)
        instance.available_uses = validated_data.get('available_uses', instance.available_uses)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.save()
        return instance

    def create(self, validated_data):
        """Crea un nuevo código de carrito."""
        cart_code = CartCode.objects.create(**validated_data)
        return cart_code