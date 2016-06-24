import urllib2
import os

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


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class LessonFiles(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="files")
    file = models.FileField(upload_to=generate_filename)

    def __str__(self):
        return self.lesson.title

    def get_filename(self):
        return os.path.basename(self.file.name)

    def get_file_size(self):
        return sizeof_fmt(self.file.size)
