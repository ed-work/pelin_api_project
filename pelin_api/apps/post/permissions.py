from rest_framework import permissions


class IsPostOwnerOrTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return (
                obj.user == request.user or
                request.user.is_teacher() and request.user == obj.group.teacher
            )
