from rest_framework import permissions
from apps.group.models import Group


class LessonPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print view.action
        if request.method == 'GET' or view.action == 'submit':
            return True

        group = Group.objects.get(pk=view.kwargs.get('group_pk'))
        return request.user.is_teacher() and request.user == group.teacher

    def has_object_permission(self, request, view, obj):
        return request.user == obj.group.teacher
