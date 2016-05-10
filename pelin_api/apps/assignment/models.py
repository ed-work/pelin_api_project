from django.db import models
from django_extensions.db.models import TitleDescriptionModel

from apps.core.models import TimeStamped, User
from apps.core.functions import generate_filename
from apps.group.models import Group


class Assignment(TimeStamped, TitleDescriptionModel):
    group = models.ForeignKey(Group)
    due_date = models.DateTimeField()
    file = models.FileField(upload_to=generate_filename, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.title, self.due_date)


# class AssignmentFiles(models.Model):
#     assignment = models.ForeignKey(Assignment, related_name="files")
#     file = models.FileField(upload_to=generate_filename)


class SubmittedAssignment(TimeStamped):
    assignment = models.ForeignKey(Assignment)
    user = models.ForeignKey(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename)

    def __unicode__(self):
        return "%s: %s" % (self.user.name, self.assignment.title)
