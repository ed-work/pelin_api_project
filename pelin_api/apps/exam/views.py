from rest_framework import viewsets
from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from .models import Exam, Question
from .serializers import ExamSerializer, QuestionSerializer
from .permissions import ExamPermission, QuestionPermission


class ExamViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = ExamSerializer

    def get_queryset(self):
        return Exam.objects.filter(group_id=self.kwargs.get('group_pk'))

    def get_permissions(self):
        if ExamPermission not in self.permission_classes:
            self.permission_classes += (ExamPermission,)
        return super(ExamViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(group=Group.objects.get(
            pk=self.kwargs.get('group_pk')))


class QuestionViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(exam_id=self.kwargs.get('exam_pk'))

    def get_permissions(self):
        if QuestionPermission not in self.permission_classes:
            self.permission_classes += (QuestionPermission,)
        return super(QuestionViewSet, self).get_permissions()
