from rest_framework import serializers
from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
