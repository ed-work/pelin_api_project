from django.db import models
from apps.core.models import TimeStamped, User, generate_filename
from apps.group.models import Group


class Post(TimeStamped):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename, blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (self.user.first_name, self.group.title)
