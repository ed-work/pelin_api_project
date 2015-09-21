from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from apps.core.models import TimeStamped, generate_filename
from apps.group.models import Group

class Lesson(TimeStamped, TitleDescriptionModel):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "%s: %s" % (self.title, self.group.title)


class LessonFiles(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="files")
    file = models.FileField(upload_to=generate_filename)
