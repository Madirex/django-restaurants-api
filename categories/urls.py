"""Category URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from categories import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))
]