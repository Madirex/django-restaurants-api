"""Reserve URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reserves import views

router = DefaultRouter()
router.register('reserves', views.ReserveViewSet, basename='reserves')

urlpatterns = [
    path('', include(router.urls))
]