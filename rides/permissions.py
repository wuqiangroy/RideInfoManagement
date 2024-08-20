# permissions.py

from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with the role 'admin' to access the API.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is an admin
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'
