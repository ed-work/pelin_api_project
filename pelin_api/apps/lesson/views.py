from rest_framework import viewsets

from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from .permissions import LessonPermission
from .serializers import LessonSerializer
from .models import Lesson


class LessonViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    filter_fields = ['title', 'description']

    def get_permissions(self):
        self.permission_classes += (LessonPermission,)
        return super(LessonViewSet, self).get_permissions()

    def get_queryset(self):
        return Lesson.objects.filter(group__pk=self.kwargs.get('group_pk')) \
            .select_related('group').prefetch_related('files')

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)
