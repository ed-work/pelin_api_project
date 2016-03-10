import urllib2
from django.db import models
from apps.core.models import TimeStamped, User
from apps.group.models import Group


def generate_filename(self, filename):
    """
    generate destination FileField filename arg to the following pattern:
    MEDIA_ROOT/<group_id>_<group_name>/filename
    """
    filename = urllib2.unquote(filename)
    return "%s_%s/%s" % (self.group.pk, self.group.title, filename)


class Post(TimeStamped):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    text = models.TextField()
    file = models.FileField(upload_to=generate_filename, blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (self.user.name, self.group.title)
