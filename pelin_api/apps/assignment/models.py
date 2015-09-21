from django.db import models
from apps.core.models import TimeStamped, User, generate_filename
from django_extensions.db.models import TitleDescriptionModel
from apps.group.models import GroupFileModel


class Assignment(TimeStamped, TitleDescriptionModel, GroupFileModel):
    due_date = models.DateTimeField()

    def __unicode__(self):
        return "%s %s" % (self.title, self.due_date)


class StudentAssignment(TimeStamped):
    assignment = models.OneToOneField(Assignment)
    student = models.OneToOneField(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename)

    def __unicode__(self):
        return "%s: %s" % (self.student.first_name, self.assignment.title)
