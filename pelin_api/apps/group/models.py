from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from apps.core.models import User, Student, Teacher


def generate_filename(self, filename):
    """
    generate destination FileField filename arg to the following pattern:
    MEDIA_ROOT/<group_name>_<group_id>/filename
    """
    return "%s_%s/%s" % (self.title, self.pk, filename)


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class GroupFileModel(models.Model):
    group = models.ForeignKey('Group')
    file = models.FileField(upload_to=generate_filename)

    class Meta:
        abstract = True


class Group(TimeStamped, TitleDescriptionModel):
    teacher = models.ForeignKey(Teacher)
    members = models.ManyToManyField(Student)


class PendingApproval(TimeStamped):
    group = models.ForeignKey(Group)
    student = models.ForeignKey(Student)


class Discussion(TimeStamped):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename, blank=True, null=True)


class Lesson(TimeStamped, TitleDescriptionModel):
    group = models.ForeignKey(Group)


class LessonFiles(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="files")
    file = models.FileField(upload_to=generate_filename)


class Assignment(TimeStamped, TitleDescriptionModel, GroupFileModel):
    due_date = models.DateTimeField()


class StudentAssignment(TimeStamped):
    assignment = models.OneToOneField(Assignment)
    student = models.OneToOneField(Student)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename)
