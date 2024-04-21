"""Restaurant Dish Link URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurant_dish_link import views

router = DefaultRouter()
router.register('restaurant_dish_link', views.RestaurantDishLinkViewSet, basename='restaurant_dish_link')

urlpatterns = [
    path('', include(router.urls))
]