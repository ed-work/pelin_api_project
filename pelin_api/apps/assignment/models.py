import urllib2

from django.db import models
from django_extensions.db.models import TitleDescriptionModel

from apps.core.models import TimeStamped, User
from apps.group.models import Group


def generate_filename(self, filename):
    filename = urllib2.unquote(filename)
    return "groups/%s/%s" % (
        self.assignment.group_id, filename)


class Assignment(TimeStamped, TitleDescriptionModel):
    group = models.ForeignKey(Group)
    due_date = models.DateTimeField()

    def __unicode__(self):
        return "%s %s" % (self.title, self.due_date)


class AssignmentFiles(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="files")
    file = models.FileField(upload_to=generate_filename)


class SubmittedAssignment(TimeStamped):
    assignment = models.ForeignKey(Assignment)
    student = models.ForeignKey(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename)

    def __unicode__(self):
        return "%s: %s" % (self.student.name, self.assignment.title)
