from rest_framework import serializers
from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation


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
