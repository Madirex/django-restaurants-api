from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users import views as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/cancel_order/<int:pk>/', user_views.UserViewSet.as_view({'post': 'cancel_order'}), name='cancel_order'),
]