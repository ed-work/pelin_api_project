from rest_framework import serializers
from apps.core.serializers import UserSerializer
from apps.group.serializers import GroupSerializer
from notifications.models import Notification

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

    class Meta:
        model = Notification
        fields = ('id', 'target', 'level', 'timestamp', 'actor',
                  'verb', 'action_object', 'unread')
