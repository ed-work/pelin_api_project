from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Conversation, Message
from apps.core.serializers import UserSerializer
from apps.core.mixins import DynamicFieldsSerializer


class ConversationSerializer(serializers.ModelSerializer):
    target_user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(ConversationSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('user')

    def get_user_id(self, obj):
        return self.get_url(obj).split('/')[-1]

    def get_target_user(self, obj):
        user = obj.get_target_user(self.user)
        if user.is_teacher():
            status = 'teacher'
        else:
            status = 'student'
        user_serializer = UserSerializer(
            user,
            fields=['name', 'url', 'photo', status],
            context={'request': self.context.get('request')})
        return user_serializer.data

    def get_url(self, obj):
        other_user = obj.get_target_user(self.user)
        if other_user.is_teacher():
            pk = other_user.teacher.username
        else:
            pk = other_user.student.nim
        return reverse('api:message-detail', kwargs={'pk': pk},
                       request=self.context.get('request'))

    def get_unread(self, obj):
        return obj.unread_by == self.context.get('request').user

    class Meta:
        model = Conversation
        fields = (
            'id', 'created_at', 'target_user', 'url',
            'user_id', 'updated_at', 'unread')


class MessageSerializer(DynamicFieldsSerializer, serializers.ModelSerializer):
    me = serializers.SerializerMethodField()
    user = UserSerializer(required=False,
                          fields=['id', 'url', 'photo'])

    def get_me(self, obj):
        return obj.user == self.context.get('user')

    class Meta:
        model = Message
        extra_kwargs = {
            'conversation': {'required': False, 'write_only': True},
            'user': {'required': False}
        }
