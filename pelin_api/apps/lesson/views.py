from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser

from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from .serializers import LessonSerializer
from .models import Lesson


class LessonViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(group__pk=self.kwargs.get('group_pk'))

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)
