from rest_framework import serializers
from .models import Dish
from categories.models import Category
from django.core.validators import MinValueValidator, FileExtensionValidator
import uuid

class DishModelSerializer(serializers.ModelSerializer):
    """Dish Model Serializer"""

    class Meta:
        """Meta class."""

        model = Dish
        fields = (
            'pk',
            'name',
            'description',
            'price',
            'dish_type',
            'ingredients',
            'calories',
            'image',
            'preparation_time',
            'category',
            'restaurants',
            'is_active',
            'created_at',
            'updated_at',
        )

class DishSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    dish_type = serializers.ChoiceField(choices=Dish.DishType.choices)
    ingredients = serializers.JSONField(default=list)
    calories = serializers.FloatField(validators=[MinValueValidator(0)])
    preparation_time = serializers.IntegerField(validators=[MinValueValidator(0)])
    category = serializers.CharField(max_length=255)
    restaurants = serializers.JSONField(default=list)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_category(self, value):
        try:
            # Verificar si la categoría existe en la base de datos
            Category.objects.get(name=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("La categoría especificada no existe.")
        return value

    def validate_restaurants(self, value):
        for item in value:
            try:
                uuid.UUID(str(item))
            except ValueError:
                raise serializers.ValidationError(f"{item} no es un UUID válido")
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(name=category)
        dish = Dish.objects.create(category=category, **validated_data)
        return dish

class DishImageUpdateSerializer(serializers.Serializer):
    image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance