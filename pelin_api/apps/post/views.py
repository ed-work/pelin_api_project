from rest_framework import viewsets

from apps.core.views import BaseLoginRequired
from .models import Post
from .serializers import GroupPostSerializer
from apps.group.permissions import IsMemberOrTeacher


class GroupPostViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = GroupPostSerializer

    def get_queryset(self):
        return Post.objects.filter(group__pk=self.kwargs.get('group_pk'))

    def get_permissions(self):
        self.permission_classes += (IsMemberOrTeacher,)
        return super(GroupPostViewSet, self).get_permissions()

