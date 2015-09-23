from rest_framework import viewsets

from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from apps.group.permissions import IsMemberOrTeacher
from .permissions import LessonPermission
from .serializers import LessonSerializer
from .models import Lesson


class LessonViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes += (IsMemberOrTeacher, LessonPermission)
        return super(LessonViewSet, self).get_permissions()

    def get_queryset(self):
        return Lesson.objects.filter(group__pk=self.kwargs.get('group_pk'))

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)
