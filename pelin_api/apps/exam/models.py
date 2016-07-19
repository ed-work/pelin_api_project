from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from apps.core.models import TimeStamped, Student
from apps.group.models import Group


class Exam(TitleDescriptionModel, TimeStamped):
    group = models.ForeignKey(Group)


class Question(models.Model):
    exam = models.ForeignKey(Exam)
    text = models.TextField()


class AnswerChoice(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField()
    _true = models.BooleanField(default=False)

    def mark_as_true(self):
        self._true = True
        self.save()


class Score(models.Model):
    student = models.ForeignKey(Student)
    exam = models.ForeignKey(Exam)
    score = models.IntegerField()


class StudentAnswer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(AnswerChoice)
    student = models.ForeignKey(Student)
