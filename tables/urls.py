"""Table URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tables import views

router = DefaultRouter()
router.register('tables', views.TableViewSet, basename='tables')

urlpatterns = [
    path('', include(router.urls))
]