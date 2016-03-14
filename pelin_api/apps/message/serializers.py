from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Conversation, Message
from apps.core.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    target_user = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(ConversationSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user
        # self.target_user = self._get_target_user(self.user)

    def get_target_user(self, obj):
        self.target_user = obj.get_target_user(self.user)
        user_serializer = UserSerializer(self.target_user)
        return user_serializer.data

    def get_url(self, obj):
        if self.target_user.is_teacher():
            pk = self.target_user.teacher.username
        else:
            pk = self.target_user.student.nim
        return reverse('api:message-detail', kwargs={'pk': pk},
                       request=self.context.get('request'))

    class Meta:
        model = Conversation
        fields = ('id', 'created_at', 'target_user', 'url')


class MessageSerializer(serializers.ModelSerializer):
    me = serializers.SerializerMethodField()

    def get_me(self, obj):
        return obj.user == self.context.get('request').user

    class Meta:
        model = Message
        extra_kwargs = {
            'conversation': {'required': False},
            'user': {'required': False}
        }
