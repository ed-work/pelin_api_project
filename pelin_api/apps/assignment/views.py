from rest_framework import viewsets
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
        return Assignment.objects.filter(group__pk=self.kwargs.get('group_pk'))

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)
