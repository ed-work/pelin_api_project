from apps.assignment.models import Assignment
from apps.assignment.serializers import AssignmentSerializer
from apps.core.mixins import DynamicFieldsSerializer
from apps.core.serializers import UserSerializer
from apps.group.serializers import GroupSerializer
from apps.lesson.models import Lesson
from apps.lesson.serializers import LessonSerializer
from apps.post.models import Comment, Post
from apps.post.serializers import GroupPostSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from rest_framework import serializers

from .realtime import fcm_async, pusher_async


class ActionObjectField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Post):
            serializer = GroupPostSerializer(value, fields=['id', 'text'])
        elif isinstance(value, Lesson):
            serializer = LessonSerializer(value, fields=['title', 'id'])
        elif isinstance(value, Assignment):
            serializer = AssignmentSerializer(value, fields=['id', 'title'])
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


def send_pusher_notif(channels, data):
    serializer = NotificationSerializer(data)
    pusher_async(channels, 'new-notif', serializer.data)


def send_fcm_notif(reg_ids, data):
    if reg_ids:
        serializer = NotificationSerializer(data)
        fcm_async(reg_ids, serializer.data)


@receiver(post_save, sender=Post)
def post_notify(sender, instance, **kwargs):
    channels = []

    members = instance.group.members
    actor = instance.user
    target = instance.group
    for member in members.exclude(id=instance.user_id):
        channels.append(str(member.id))
        notif = Notification.objects.create(
            actor=actor,
            verb='mengirim post',
            target=target,
            recipient=member)
        notif.save()
        send_pusher_notif(channels, notif)
    if instance.user_id != instance.group.teacher_id:
        channels.append(str(instance.group.teacher_id))
        notif = Notification.objects.create(
            actor=actor,
            verb='mengirim post',
            target=target,
            recipient=target.teacher)
        notif.save()
        send_pusher_notif(channels, notif)


@receiver(post_save, sender=Comment)
def comment_notify(sender, instance, **kwargs):
    if instance.user_id != instance.post.user_id:
        notif = Notification.objects.create(
            actor=instance.user,
            verb='mengomentari postingan',
            target=instance.post.group,
            action_object=instance.post,
            recipient=instance.post.user)
        notif.save()
        send_pusher_notif(str(notif.recipient_id), notif)


@receiver(post_save, sender=Lesson)
def lesson_notify(sender, instance, **kwargs):
    group = instance.group
    members = group.members
    if members.exists():
        channels = []
        for member in group.members.all():
            channels.append(str(member.id))
            notif = Notification.objects.create(
                actor=group.teacher,
                verb='menambahkan materi',
                action_object=instance,
                target=group,
                recipient=member)
            notif.save()
        send_pusher_notif(channels, notif)

        reg_ids = members.values_list('reg_id', flat=True).exclude(reg_id=None)
        send_fcm_notif(reg_ids, notif)


@receiver(post_save, sender=Assignment)
def assignment_notify(sender, instance, **kwargs):
    group = instance.group
    members = group.members
    if members.exists():
        channels = []
        for member in members.all():
            channels.append(str(member.id))
            notif = Notification.objects.create(
                actor=group.teacher,
                verb='menambahkan tugas',
                action_object=instance,
                target=group,
                recipient=member)
            notif.save()
        send_pusher_notif(channels, notif)

        reg_ids = members.values_list('reg_id', flat=True).exclude(reg_id=None)
        send_fcm_notif(reg_ids, notif)
