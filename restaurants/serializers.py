from rest_framework import serializers
from .models import Restaurant
from utils.validators import validate_address
from rest_framework.exceptions import ValidationError
from tables.serializers import TableSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    """Serializador del modelo Restaurant."""
    tables = TableSerializer(many=True, read_only=True)
    address = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        """Clase Meta."""
        model = Restaurant
        fields = (
            'pk',
            'name',
            'address',
            'calendar',
            'tables',
            'active',
            'created_at',
            'updated_at',
        )
    def validate_address(self, value):
        """Validación para el campo address."""
        if not isinstance(value, dict):
            raise ValidationError("La dirección debe ser un objeto JSON.")
        validate_address(value)
        return value