from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Conversation, Message
from apps.core.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    target_user = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(ConversationSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('user')

    def get_target_user(self, obj):
        if self.user.is_teacher():
            status = 'teacher'
        else:
            status = 'student'
        user_serializer = UserSerializer(
            self.user,
            fields=['id', 'name', 'url', 'photo', status],
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

    class Meta:
        model = Conversation
        fields = ('id', 'created_at', 'target_user', 'url')


class MessageSerializer(serializers.ModelSerializer):
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
