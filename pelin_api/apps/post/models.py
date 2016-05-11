from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from notifications.signals import notify

from apps.core.models import TimeStamped, User
from apps.core.functions import generate_filename
from apps.group.models import Group


class Post(TimeStamped):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename, blank=True, null=True)
    votes = models.ManyToManyField(User, related_name='user_votes')

    @property
    def get_votes_count(self):
        return self.votes.count()

    def __unicode__(self):
        return self.text


class Comment(TimeStamped):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField()


@receiver(post_save, sender=Post)
def post_notify(sender, instance, **kwargs):
    for member in instance.group.members.exclude(id=instance.user_id):
        notify.send(
            instance.user,
            verb='mengirim post',
            target=instance.group,
            recipient=member)


@receiver(post_save, sender=Comment)
def comment_notify(sender, instance, **kwargs):
    notify.send(
        instance.user,
        verb='mengomentari postingan',
        target=instance.post.group,
        action_object=instance.post,
        recipient=instance.post.user)
