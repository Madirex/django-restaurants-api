"""Restaurant URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurants import views

router = DefaultRouter()
router.register('restaurants', views.RestaurantViewSet, basename='restaurants')

urlpatterns = [
    path('', include(router.urls)),
    path('menu/', views.MenuView.as_view(), name='menu'),
]