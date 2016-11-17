from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_extensions.db.models import TitleDescriptionModel
from notifications.signals import notify

from apps.core.models import User, TimeStamped, generate_filename


class GroupFileModel(models.Model):
    group = models.ForeignKey('Group')
    file = models.FileField(upload_to=generate_filename)

    class Meta:
        abstract = True


class Group(TimeStamped, TitleDescriptionModel):
    SEMESTER_CHOICES = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
        (6, 'VI'),
        (7, 'VII'),
        (8, 'VII'),
    )

    teacher = models.ForeignKey(User, related_name='group_teacher')
    members = models.ManyToManyField(User, related_name='group_members')
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    major = models.CharField(max_length=5)

    def __unicode__(self):
        return self.title


class PendingApproval(TimeStamped):
    group = models.ForeignKey(Group, related_name='pendings')
    user = models.ForeignKey(User, related_name='pending_approval')

    def approve(self):
        self.group.members.add(self.user)
        self.group.save()
        self.delete()

    def __unicode__(self):
        return "%s: %s" % (self.group.title, self.user.name)


@receiver(post_save, sender=PendingApproval)
def pending_notify(sender, instance, **kwargs):
    notify.send(
        instance.user,
        verb='meminta bergabung',
        target=instance.group,
        recipient=instance.group.teacher)
