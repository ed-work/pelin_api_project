import urllib2

from django.db import models
from django_extensions.db.models import TitleDescriptionModel

from apps.core.models import TimeStamped, User
from apps.group.models import GroupFileModel, Group


def generate_filename(self, filename):
    """
    generate destination FileField filename arg to the following pattern:
    MEDIA_ROOT/<group_name>_<group_id>/filename
    """
    filename = urllib2.unquote(filename)
    return "%s_%s/%s" % (
    self.assignment.group.pk, self.assignment.group.title, filename)


class Assignment(TimeStamped, TitleDescriptionModel):
    group = models.ForeignKey(Group)
    due_date = models.DateTimeField()

    def __unicode__(self):
        return "%s %s" % (self.title, self.due_date)


class AssignmentFiles(models.Model):
    assignment = models.ForeignKey(Assignment)
    file = models.FileField(upload_to=generate_filename)


class StudentAssignment(TimeStamped):
    assignment = models.OneToOneField(Assignment)
    student = models.OneToOneField(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename)

    def __unicode__(self):
        return "%s: %s" % (self.student.first_name, self.assignment.title)
