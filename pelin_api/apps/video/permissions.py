from rest_framework.permissions import BasePermission, SAFE_METHODS


class VideoPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PATCH']:
            return (
                obj.user == request.user or
                request.user.is_staff or
                request.user.is_admin
            )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_admin or\
                request.user.is_staff or\
                request.user.is_teacher()
        return True
