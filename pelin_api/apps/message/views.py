from rest_framework import viewsets, status, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from apps.core.models import User
from apps.core.views import BaseLoginRequired
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from django.db.models import Q


class ConversationViewSet(BaseLoginRequired,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(
            Q(user_1=self.request.user) | Q(user_2=self.request.user)
        ).order_by('-created_at')

    def get_conversation(self):
        try:
            conversation = self.get_object()
        except:
            try:
                target_user = User.objects.get_with(self.kwargs.get('pk'))
                conversation = Conversation.objects.get(
                    (Q(user_1=self.request.user) & Q(user_2=target_user)) |
                    (Q(user_1=target_user) & Q(user_2=self.request.user))
                )
            except Conversation.DoesNotExist:
                conversation = None

        return conversation

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_conversation()
        print conversation

        if conversation:
            messages = Message.objects.filter(
                conversation=conversation).order_by('-sent')
            messages_page = self.paginate_queryset(messages)
            serializer = MessageSerializer(messages_page, many=True,
                                           context={'request': request})
            return self.get_paginated_response(serializer.data)
        else:
            return super(ConversationViewSet, self).retrieve(request, *args,
                                                             **kwargs)

    @detail_route(methods=['POST'])
    def reply(self, request, pk):
        conversation = self.get_conversation()
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, conversation=conversation)
            return Response({'success': 'Your message has sent.'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
