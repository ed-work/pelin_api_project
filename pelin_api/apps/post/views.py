from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from apps.group.permissions import IsMemberOrTeacher
from apps.post.permissions import IsPostOwnerOrTeacher
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import Comment
from .serializers import GroupPostSerializer, CommentSerializer


class GroupPostViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = GroupPostSerializer
    filter_fields = ['user', 'created_at', 'text']

    def initial(self, request, *args, **kwargs):
        super(GroupPostViewSet, self).initial(request, *args, **kwargs)
        self.group = self.get_group()

    def get_group(self):
        return get_object_or_404(Group, pk=self.kwargs.get('group_pk'))

    def get_queryset(self):
        return self.group.post_set\
            .select_related('user', 'user__teacher', 'user__student')\
            .prefetch_related('votes')\
            .order_by('-created_at')

    def get_permissions(self):
        permission = (IsMemberOrTeacher,)
        if self.action not in ('retrieve', 'vote'):
            permission += (IsPostOwnerOrTeacher,)
        self.permission_classes += permission
        return super(GroupPostViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, group=self.group)

    @detail_route(methods=['GET'], permission_classes=[IsMemberOrTeacher])
    def vote(self, request, group_pk=None, pk=None):
        user = request.user
        post = self.get_object()
        if user not in post.votes.all():
            post.votes.add(user)
            return Response({'msg': 'voted'})
        else:
            post.votes.remove(user)
            return Response({'msg': 'unvote'})


class CommentViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__pk=self.kwargs.get('post_pk')
        ).select_related('user').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        post__pk=self.kwargs.get('post_pk'))
