from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.group.models import Group
from apps.post.models import Post


class GroupPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_teacher()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return (
                obj.teacher == request.user or
                obj.group.teacher == request.user
            )

        return request.user.is_teacher()


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_teacher()


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher()


class IsMemberOrTeacherGroup(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.teacher or request.user in obj.members.all()


class IsTeacherGroup(BasePermission):
    def has_permission(self, request, view):
        group = Group.objects.get(pk=view.kwargs.get('group_pk'))
        return request.user == group.teacher


class IsMemberOrTeacher(BasePermission):
    # def has_permission(self, request, view):
    #     group = Group.objects.prefetch_related('members').select_related('teacher').get(pk=view.kwargs.get('group_pk'))
    #     return (
    #         request.user in group.members.all() or request.user == group.teacher
    #     )
    def has_object_permission(self, request, view, obj):
        u = request.user
        if type(obj) == Post:
            obj = obj.group

        return u in obj.members.all() or u == obj.teacher
