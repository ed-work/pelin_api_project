from rest_framework import permissions


class GroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_teacher()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return obj.teacher == request.user

        return  request.user.is_teacher()
