from django.db import models
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
