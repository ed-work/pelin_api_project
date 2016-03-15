from rest_framework import viewsets, status, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from apps.core.models import User
from apps.core.views import BaseLoginRequired
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation
from django.db.models import Q


class ConversationViewSet(BaseLoginRequired,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ConversationSerializer

    def initial(self, request, *args, **kwargs):
        super(ConversationViewSet, self).initial(request, *args, **kwargs)
        self.user = self.request.user

    def get_queryset(self):
        return Conversation.objects.filter(
            Q(user_1=self.request.user) | Q(user_2=self.request.user))\
            .select_related('user_1')\
            .select_related('user_2').order_by('-created_at')

    def get_serializer_context(self):
        c = super(ConversationViewSet, self).get_serializer_context()
        c['user'] = self.request.user
        return c

    def get_object(self):
        other_user = User.objects.get_with(self.kwargs.get('pk'))
        try:
            conversation = Conversation.objects.get(
                (Q(user_1=self.request.user) & Q(user_2=other_user)) |
                (Q(user_1=other_user) & Q(user_2=self.request.user))
            )
        except Conversation.DoesNotExist:
            conversation = None
            # conversation = Conversation.objects.create(
            #     user_1=self.request.user,
            #     user_2=other_user)

        return conversation

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()

        if conversation:
            # TODO: get messages visible_to certain user
            messages = conversation.message_set.select_related('user')\
                .select_related('user')\
                .order_by('-sent')
            # messages_page = self.paginate_queryset(messages)
            serializer = MessageSerializer(
                messages, many=True,
                context={'request': self.request, 'user': self.user})
            # return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        else:
            # return super(ConversationViewSet, self).retrieve(request, *args,
            #                                                  **kwargs)
            return Response([])

    @detail_route(methods=['POST'])
    def reply(self, request, pk):
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, conversation=conversation)
            return Response({'text': request.data.get('text')},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
