from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .serializers import GroupSerializer
from .models import Group, PendingApproval
from .permissions import GroupPermission, IsStudent
from apps.core.views import BaseLoginRequired
from apps.core.serializers import UserSerializer


class GroupViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_permissions(self):
        self.permission_classes += (GroupPermission,)
        return super(GroupViewSet, self).get_permissions()

    @detail_route()
    def members(self, request, pk):
        members = self.get_object().members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'], permission_classes=[IsStudent])
    def join(self, request, pk):
        PendingApproval.objects.create(
            student=request.user, group=self.get_object()
        )
        return Response(
            {'success': 'Wait for approval'},
            status=status.HTTP_200_OK
        )
