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
    # TODO: ENLAZAR CON PLATO (DISH) -- user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(max_length=250)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, data):
        exp = Category.objects.create(**data)
        return exp