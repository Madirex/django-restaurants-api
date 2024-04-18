from rest_framework import serializers
from restaurant_dish_link.models import RestaurantDishLink

class RestaurantDishLinkSerializer(serializers.ModelSerializer):
    """Serializer for RestaurantDishLink model"""

    class Meta:
        """Meta class"""
        model = RestaurantDishLink
        fields = (
            'id',
            #'restaurant',
            'dish',
            'stock',
        )

    def validate_stock(self, value):
        """Validation for stock field"""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def validate(self, data):
        """Additional validation for the serializer"""
        return data
