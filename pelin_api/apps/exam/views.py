from rest_framework import viewsets
from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from .models import Exam
from .serializers import ExamSerializer
from .permissions import ExamPermission


class ExamViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = ExamSerializer

    def get_queryset(self):
        return Exam.objects.filter(group__pk=self.kwargs.get('group_pk'))

    def get_permissions(self):
        if ExamPermission not in self.permission_classes:
            self.permission_classes += (ExamPermission,)
        return super(ExamViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(group=Group.objects.get(
            pk=self.kwargs.get('group_pk')))
