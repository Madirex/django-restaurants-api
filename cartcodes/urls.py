"""CartCode URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cartcodes import views

router = DefaultRouter()
router.register('cartcodes', views.CartCodeViewSet, basename='cartcodes')

urlpatterns = [
    path('', include(router.urls))
]