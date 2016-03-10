from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from apps.group.permissions import IsMemberOrTeacher
from apps.post.permissions import IsPostOwnerOrTeacher
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Post
from .serializers import GroupPostSerializer


class GroupPostViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = GroupPostSerializer
    filter_fields = ['user', 'created_at', 'text']

    def get_queryset(self):
        return Post.objects.filter(
            group__pk=self.kwargs.get('group_pk')
        ).order_by('-created_at')

    def get_permissions(self):
        permission = (IsMemberOrTeacher,)
        if self.action != 'retrieve':
            permission += (IsPostOwnerOrTeacher,)
        self.permission_classes += permission
        return super(GroupPostViewSet, self).get_permissions()

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(user=self.request.user, group=group)

    @detail_route(methods=['GET'])
    def vote(self, request, group_pk=None, pk=None):
        return Response({'msg': 'voted'})
