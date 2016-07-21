import ujson
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from apps.core.views import BaseLoginRequired
from .models import Exam, Question, StudentAnswer, Score
from .serializers import ExamSerializer, QuestionSerializer, ScoreSerializer
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
        serializer.save(group_id=self.kwargs.get('group_pk'))

    @detail_route(methods=['post'])
    def answer(self, request, group_pk, pk):
        if StudentAnswer.objects.filter(
                user=request.user).exists():
            return Response(
                {'error': 'You have been answered this exam.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            answers = ujson.loads(request.POST.get('answer'))
            bulks = []
            for i in answers:
                bulks.append(
                    StudentAnswer(
                        question_id=int(i),
                        user=request.user,
                        answer=answers[i])
                )
            student_answers = StudentAnswer.objects.bulk_create(bulks)

            try:
                trues = [i for i in student_answers if i.is_true]
                exam = Exam.objects.get(id=pk)
                score = float(len(trues)) / exam.question_set.count()
                Score.objects.create(
                    user=request.user,
                    score=score,
                    exam=exam)
            except Exception, e:
                print e
                return Response(
                    {'error': 'bad request'},
                    status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': 'success'})
        except Exception, e:
            print e
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'])
    def scores(self, request, group_pk, pk):
        scores = Score.objects.filter(exam_id=pk)\
            .select_related('user')\
            .select_related('user__student')
        serializer = ScoreSerializer(scores, many=True)
        return Response(data=serializer.data)


class QuestionViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(exam_id=self.kwargs.get('exam_pk'))

    def get_permissions(self):
        if QuestionPermission not in self.permission_classes:
            self.permission_classes += (QuestionPermission,)
        return super(QuestionViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(exam_id=self.kwargs.get('exam_pk'))
