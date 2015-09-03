from rest_framework.permissions import BasePermission, SAFE_METHODS


class GroupPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_teacher()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return obj.teacher == request.user or obj.group.teacher == request.user

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