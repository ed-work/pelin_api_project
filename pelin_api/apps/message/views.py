from rest_framework import viewsets
from apps.core.views import BaseLoginRequired
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation
from django.db.models import Q


class ConversationViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(
            Q(user_1=self.request.user) | Q(user_2=self.request.user))
