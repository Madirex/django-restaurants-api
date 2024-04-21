"""Order Lines URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from order_lines import views

router = DefaultRouter()
router.register('order_lines', views.OrderLineViewSet, basename='order_lines')

urlpatterns = [
    path('', include(router.urls))
]