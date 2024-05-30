"""Schedule URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from schedules import views

router = DefaultRouter()
router.register('schedules', views.ScheduleViewSet, basename='schedules')

urlpatterns = [
    path('', include(router.urls))
]