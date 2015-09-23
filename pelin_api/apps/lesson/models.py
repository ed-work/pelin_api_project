import urllib2
from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from apps.core.models import TimeStamped
from apps.group.models import Group


def generate_filename(self, filename):
    """
    generate destination FileField filename arg to the following pattern:
    MEDIA_ROOT/<group_name>_<group_id>/filename
    """
    filename = urllib2.unquote(filename)
    return "%s_%s/%s" % (self.pk, self.lesson.group, filename)


class Lesson(TimeStamped, TitleDescriptionModel):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "%s: %s" % (self.title, self.group.title)


class LessonFiles(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="files")
    file = models.FileField(upload_to=generate_filename)
