from rest_framework import serializers
from .models import Restaurant
from address.validators import validate_address
from rest_framework.exceptions import ValidationError

class RestaurantSerializer(serializers.ModelSerializer):
    address = serializers.JSONField(required=False, allow_null=True)
    class Meta:
        model = Restaurant
        fields = (
            'pk',
            'name',
            'address',
            'calendar',
            'active',
            'created_at',
            'updated_at',
        )
    def validate_address(self, value):
        if not isinstance(value, dict):
            raise ValidationError("La dirección debe ser un objeto JSON.")
        validate_address(value)
        return value