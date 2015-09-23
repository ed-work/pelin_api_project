from rest_framework import viewsets
from apps.core.views import BaseLoginRequired
from .serializers import LessonSerializer
from .models import Lesson


class LessonViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(group__pk=self.kwargs.get('group_pk'))
