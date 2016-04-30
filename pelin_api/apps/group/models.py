from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from apps.core.models import User, TimeStamped, generate_filename


class GroupFileModel(models.Model):
    group = models.ForeignKey('Group')
    file = models.FileField(upload_to=generate_filename)

    class Meta:
        abstract = True


class Group(TimeStamped, TitleDescriptionModel):
    teacher = models.ForeignKey(User, related_name='group_teacher')
    members = models.ManyToManyField(User, related_name='group_members')

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
