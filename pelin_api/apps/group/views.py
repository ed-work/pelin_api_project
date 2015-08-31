from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, DestroyModelMixin

from .serializers import GroupSerializer, PendingApproveSerializer
from .models import Group, PendingApproval
from .permissions import GroupPermission, IsStudent, IsTeacher
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

    @detail_route(permission_classes=[IsStudent])
    def join(self, request, pk):
        if PendingApproval.objects.filter(student=request.user).exists():
            msg = {'error': 'Your join request is pending'}
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            PendingApproval.objects.create(
                student=request.user, group=self.get_object()
            )
            msg = {'success': 'Wait for approval'}
            status_code = status.HTTP_200_OK
        return Response(msg, status=status_code)


class PendingApprovalViewSet(BaseLoginRequired, ListModelMixin,
                             DestroyModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = PendingApproveSerializer
    queryset = PendingApproval.objects.all()

    def list(self, request, *args, **kwargs):
        pendings = self.queryset.filter(group__pk=kwargs.get('group_pk'))
        serializer = PendingApproveSerializer(pendings, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        self.permission_classes += (GroupPermission,)
        return super(PendingApprovalViewSet, self).get_permissions()

    @detail_route(methods=['post'], permission_classes=[IsTeacher])
    def approve(self, request, group_pk, pk):
        obj = self.get_object()
        group = Group.objects.get(pk=group_pk)
        group.members.add(obj.student)
        self.perform_destroy(obj)

        return Response
