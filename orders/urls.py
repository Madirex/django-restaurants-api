"""Order URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from orders import views

router = DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))
]