from rest_framework import viewsets

from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from apps.post.permissions import IsPostOwnerOrTeacher
from .models import Post
from .serializers import GroupPostSerializer
from apps.group.permissions import IsMemberOrTeacher


class GroupPostViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = GroupPostSerializer

    def get_queryset(self):
        return Post.objects.filter(
            group__pk=self.kwargs.get('group_pk')
        ).order_by('-created_at')

    def get_permissions(self):
        self.permission_classes += (IsMemberOrTeacher, IsPostOwnerOrTeacher)
        return super(GroupPostViewSet, self).get_permissions()

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(user=self.request.user, group=group)
