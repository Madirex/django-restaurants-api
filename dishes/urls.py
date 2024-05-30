"""Dish URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from dishes import views

router = DefaultRouter()
router.register('dishes', views.DishViewSet, basename='dishes')

urlpatterns = [
    path('', include(router.urls))
]