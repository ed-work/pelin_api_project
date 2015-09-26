import datetime
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from apps.group.permissions import IsMemberOrTeacher
from apps.lesson.permissions import LessonPermission
from .serializers import AssignmentSerializer
from .models import Assignment


class AssignmentViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        self.permission_classes += (IsMemberOrTeacher, LessonPermission)
        return super(AssignmentViewSet, self).get_permissions()

    def get_queryset(self):
        assignments = Assignment.objects.filter(
            group__pk=self.kwargs.get('group_pk'))
        if not self.request.user.is_teacher():
            return assignments.filter(due_date__gt=datetime.datetime.now())
        return assignments

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)

    @detail_route()
    def submit(self, request, group_pk, pk):
        # TODO: student assignment
        pass
