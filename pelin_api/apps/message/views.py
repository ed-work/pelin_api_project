from rest_framework import viewsets
from rest_framework.response import Response
from apps.core.models import User
from apps.core.views import BaseLoginRequired
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from django.db.models import Q


class ConversationViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(
            Q(user_1=self.request.user) | Q(user_2=self.request.user))

    def retrieve(self, request, *args, **kwargs):
        try:
            conversation = self.get_object()
        except:
            try:
                target_user = User.objects.get_with(kwargs.get('pk'))
                conversation =  Conversation.objects.get(
                    (Q(user_1=request.user) & Q(user_2=target_user)) |
                    (Q(user_1=target_user) & Q(user_2=request.user))
                )
            except:
                conversation = None

        if conversation:
            messages = Message.objects.filter(conversation=conversation)
            messages_page = self.paginate_queryset(messages)
            serializer = MessageSerializer(messages_page, many=True)
            return Response(serializer.data)
        else:
            return super(ConversationViewSet, self).retrieve(request, *args, **kwargs)

