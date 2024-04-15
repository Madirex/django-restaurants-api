"""User permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from users.models import User


class IsStandardUser(BasePermission):
    """Allow access."""

    def has_permission(self, request, view):

        try:
            user = User.objects.get(
                email=request.user,
            )
        except User.DoesNotExist:
            return False
        return True

class IsAdminUser(BasePermission):
    """Allow access."""

    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                is_admin=True
            )
        except User.DoesNotExist:
            return False
        return True