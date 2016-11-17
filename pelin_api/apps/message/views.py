from rest_framework import viewsets, status, mixins
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from apps.core.models import User
from apps.core.views import BaseLoginRequired
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation
from django.db.models import Q


class ConversationViewSet(BaseLoginRequired,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ConversationSerializer

    def initial(self, request, *args, **kwargs):
        super(ConversationViewSet, self).initial(request, *args, **kwargs)
        self.user = self.request.user

    def get_queryset(self):
        user = self.user
        return Conversation.objects\
            .filter(
                (Q(sender=user) | Q(reciever=user)) &
                (Q(message__isnull=False)) &
                (Q(message__visible_to=None) | Q(message__visible_to=user))
            )\
            .select_related('sender', 'reciever')\
            .distinct().order_by('-updated_at')

    def get_serializer_context(self):
        c = super(ConversationViewSet, self).get_serializer_context()
        c['user'] = self.request.user
        return c

    def get_object(self):
        other_user = User.objects.get_with(self.kwargs.get('pk'))
        try:
            conversation = Conversation.objects.get(
                (Q(sender=self.request.user) & Q(reciever=other_user)) |
                (Q(sender=other_user) & Q(reciever=self.request.user))
            )
        except Conversation.DoesNotExist:
            conversation = None

        return conversation

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.clear_message_history(self.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()

        if conversation:
            conversation.unread_by = None
            conversation.save()
            messages = conversation.message_set \
                .filter(Q(visible_to=self.user) | Q(visible_to=None)) \
                .select_related('user') \
                .select_related('user') \
                .order_by('sent')
            serializer = MessageSerializer(
                messages, many=True,
                remove_fields=['visible_to'],
                context={'request': self.request, 'user': self.user})
            return Response(serializer.data)
        else:
            return Response([])

    def list(self, request, *args, **kwargs):
        if 'status' in request.query_params:
            return Response({'unread': 10})

        return super(ConversationViewSet, self).list(request, *args, **kwargs)

    @detail_route(methods=['POST'])
    def reply(self, request, pk):
        conversation = self.get_object()

        if not conversation:
            other_user = User.objects.get_with(self.kwargs.get('pk'))
            conversation = conversation = Conversation.objects.create(
                sender=self.request.user,
                reciever=other_user,
                unread_by=other_user)
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, conversation=conversation)
            return Response({'text': request.data.get('text')},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['GET'])
    def unread_count(self, request):
        count = self.get_queryset().filter(unread_by=request.user).count()
        return Response({'count': count})
