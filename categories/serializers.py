# Django REST Framework
from rest_framework import serializers
# Model
from categories.models import Category

class CategoryModelSerializer(serializers.ModelSerializer):
    """Category Model Serializer"""

    class Meta:
        """Meta class."""

        model = Category
        fields = (
            'pk',
            'name',
            'is_active',
            'created_at',
            'updated_at',
        )

class CategorySerializer(serializers.Serializer):
    """Serializer para crear/actualizar categorías"""
    name = serializers.CharField(max_length=250)
    is_active = serializers.BooleanField(default=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value):
        """Comprueba que sea un nombre único."""
        value = value.lower()
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")

        return value

    def create(self, data):
        """Crea una nueva categoría."""
        exp = Category.objects.create(**data)
        return exp