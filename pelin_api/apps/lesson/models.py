import urllib2

from django.db import models

from django_extensions.db.models import TitleDescriptionModel

from apps.core.models import TimeStamped
from apps.group.models import Group


def generate_filename(self, filename):
    filename = urllib2.unquote(filename)
    return "groups/%s/%s" % (self.lesson.group_id, filename)


class Lesson(TimeStamped, TitleDescriptionModel):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "%s: %s" % (self.title, self.group_id)


class LessonFiles(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="files")
    file = models.FileField(upload_to=generate_filename)
