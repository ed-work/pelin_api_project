import urllib2

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from django_extensions.db.models import TitleDescriptionModel
from notifications.signals import notify

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


@receiver(post_save, sender=Lesson)
def lesson_notify(sender, instance, **kwargs):
    if instance.group.members.exists():
        for member in instance.group.members.all():
            notify.send(
                instance.group.teacher,
                verb='menambahkan materi',
                action_object=instance,
                target=instance.group,
                recipient=member)
