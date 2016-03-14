from django.db import models
from apps.core.models import User


STATUS_CHOICES = (
    ('s', 'Send'),
    ('r', 'Read'),
)


class Conversation(models.Model):
    user_1 = models.ForeignKey(User, related_name='_from')
    user_2 = models.ForeignKey(User, related_name='_to')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s:%s" % (self.user_1.name, self.user_2.name)

    def get_target_user(self, user):
        if self.user_1 == user:
            return self.user_2
        return self.user_1


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    user = models.ForeignKey(User)
    text = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='s')

    def __unicode__(self):
        return "%s: %s" % (self.user.name, self.text)
