"""Calendar URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from calendars import views

router = DefaultRouter()
router.register('calendars', views.CalendarViewSet, basename='calendars')

urlpatterns = [
    path('', include(router.urls))
]