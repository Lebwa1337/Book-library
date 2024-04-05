from rest_framework import permissions


class IsAdminReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if bool(request.user and request.user.is_staff):
            return True
        return False
