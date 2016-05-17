from rest_framework import serializers
from apps.core.serializers import UserSerializer
from apps.group.serializers import GroupSerializer
from notifications.models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from .realtime import pusher_async
from apps.post.models import Post
from apps.lesson.models import Lesson
from apps.assignment.models import Assignment

from apps.post.serializers import GroupPostSerializer
from apps.lesson.serializers import LessonSerializer
from apps.assignment.serializers import AssignmentSerializer

from apps.core.mixins import DynamicFieldsSerializer


class ActionObjectField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Post):
            serializer = GroupPostSerializer(value)
        elif isinstance(value, Lesson):
            serializer = LessonSerializer(value, fields=['title', 'id'])
        elif isinstance(value, Assignment):
            serializer = AssignmentSerializer(value)
        return serializer.data


class NotificationSerializer(DynamicFieldsSerializer,
                             serializers.ModelSerializer):
    actor = UserSerializer(fields=['name', 'photo'])
    target = GroupSerializer(fields=['title', 'id'])
    action_object = ActionObjectField(read_only=True)
    action_type = serializers.SerializerMethodField()

    def get_action_type(self, obj):
        if isinstance(obj.action_object, Lesson):
            return 'lesson'
        elif isinstance(obj.action_object, Post):
            return 'post'
        elif isinstance(obj.action_object, Assignment):
            return 'assignment'
        else:
            return None

    class Meta:
        model = Notification
        fields = ('id', 'target', 'level', 'timestamp', 'actor',
                  'verb', 'action_object', 'unread', 'action_type')


@receiver(post_save, sender=Notification)
def notif_post_save(sender, instance, **kwargs):
    serializer = NotificationSerializer(instance)
    pusher_async(str(instance.recipient_id), 'new-notif', serializer.data)
