from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from . import serializers as group_serializers
from . import models as group_models
from . import permissions as group_permissions
from apps.core.views import BaseLoginRequired
from apps.core.serializers import UserSerializer


class GroupViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = group_serializers.GroupSerializer
    queryset = group_models.Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_permissions(self):
        self.permission_classes += (group_permissions.GroupPermission,)
        return super(GroupViewSet, self).get_permissions()

    @detail_route()
    def members(self, request, pk):
        members = self.get_object().members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)
