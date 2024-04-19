from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'pk',
            'name',
            'address',
            #TODO: 'menu',
            #TODO: 'tables',
            'active',
            'created_at',
            'updated_at',
        )
