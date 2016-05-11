from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_extensions.db.models import TitleDescriptionModel
from notifications.signals import notify

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


@receiver(post_save, sender=Assignment)
def assignment_notify(sender, instance, **kwargs):
    if instance.group.members.exists():
        for member in instance.group.members.all():
            notify.send(
                instance.group.teacher,
                verb='menambahkan tugas',
                action_object=instance,
                target=instance.group,
                recipient=member)
