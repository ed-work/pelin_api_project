from django.db import models
from apps.core.models import User


STATUS_CHOICES = (
    ('s', 'Send'),
    ('r', 'Read'),
)

class Conversation(models.Model):
    user_1 = models.ForeignKey(User)
    user_2 = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    user = models.ForeignKey(User)
    text = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='s')
