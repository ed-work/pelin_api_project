from rest_framework import permissions


class CustomUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return request.user.is_superuser

        return (obj == request.user) or request.user.is_superuser


class CreateUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.method == 'POST' and (
                not request.user.is_authenticated() or request.user.is_superuser))
