from django.db import models
from apps.core.models import User


STATUS_CHOICES = (
    ('s', 'Send'),
    ('r', 'Read'),
)


class Conversation(models.Model):
    sender = models.ForeignKey(User, related_name='conversation_sender')
    reciever = models.ForeignKey(User, related_name='conversation_reciever')
    unread_by = models.ForeignKey(
        User, related_name='conversation_unread_by', null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s:%s" % (self.sender.name, self.reciever.name)

    def get_target_user(self, user):
        return self.reciever if user == self.sender else self.sender

    def clear_message_history(self, by_user):
        other_user = self.get_target_user(by_user)
        messages = self.message_set.filter(~models.Q(visible_to=None))
        if messages:
            self.message_set.all().delete()
        else:
            self.message_set.update(visible_to=other_user)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    user = models.ForeignKey(User)
    visible_to = models.ForeignKey(User, null=True, default=None,
                                   related_name='message_visible_to')
    text = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='s')

    def __unicode__(self):
        return "%s: %s" % (self.user.name, self.text)

    def save(self, **kwargs):
        super(Message, self).save(kwargs)
        self.conversation.updated_at = self.sent
        self.conversation.unread_by = self.conversation.get_target_user(
            self.user)
        self.conversation.save()
