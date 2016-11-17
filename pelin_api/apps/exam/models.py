from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from apps.core.models import TimeStamped, User
from apps.group.models import Group


class Exam(TitleDescriptionModel, TimeStamped):
    group = models.ForeignKey(Group)
    duration = models.IntegerField()

    def __str__(self):
        return self.title

    def get_score(self, user):
        try:
            return self.score_set.get(exam_id=self.id, user=user).score
        except Exception, e:
            print e
            return None


class Question(models.Model):
    exam = models.ForeignKey(Exam)
    text = models.TextField()

    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()

    answer_key = models.CharField(max_length=1)

    def __str__(self):
        return self.text


# class AnswerChoice(models.Model):
#     question = models.ForeignKey(Question)
#     text = models.TextField()
#     _true = models.BooleanField(default=False)

#     def mark_as_true(self):
#         self._true = True
#         self.save()


class Score(models.Model):
    user = models.ForeignKey(User)
    exam = models.ForeignKey(Exam)
    score = models.FloatField()

    def __str__(self):
        return "%s: %s" % (self.user.student.nim, self.score)


class StudentAnswer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=1)
    user = models.ForeignKey(User)

    @property
    def is_true(self):
        return self.answer == self.question.answer_key

    def __str__(self):
        return "%s: %s" % (self.user.student.nim, self.answer)
