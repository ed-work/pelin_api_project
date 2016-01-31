from rest_framework import viewsets, status, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, DestroyModelMixin

from apps.core.models import User, Student
from .serializers import GroupSerializer, PendingApproveSerializer
from .models import Group, PendingApproval
from .permissions import GroupPermission, IsStudent, IsMemberOrTeacherGroup, \
    IsTeacherGroup
from apps.core.views import BaseLoginRequired
from apps.core.serializers import UserSerializer
from apps.core.cache import CachedResourceMixin


class GroupViewSet(BaseLoginRequired, CachedResourceMixin,
                   viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all().select_related('teacher',
                                                  'teacher__teacher')
    filter_fields = ['id', 'teacher', 'members', 'title']

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_permissions(self):
        self.permission_classes += (GroupPermission,)
        return super(GroupViewSet, self).get_permissions()

    @detail_route(methods=['get'])
    def members(self, request, pk):
        members = self.get_object().members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

    @detail_route(permission_classes=[permissions.IsAuthenticated, IsStudent])
    def join(self, request, pk):
        if request.user.pk in self.get_object().pendings.values_list('student',
                                                                     flat=True):
            msg = {'error': 'Your join request in this group is pending.'}
            status_code = status.HTTP_400_BAD_REQUEST
        elif self.get_object().members.filter(pk=request.user.pk).exists():
            msg = {'error': 'You are member in this group.'}
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            PendingApproval.objects.create(
                student=request.user, group=self.get_object()
            )
            msg = {'success': 'Wait for approval.'}
            status_code = status.HTTP_200_OK
        return Response(msg, status=status_code)

    @detail_route(permission_classes=[IsStudent])
    def leave(self, request, pk):
        if self.get_object().members.filter(pk=request.user.pk).exists():
            self.get_object().members.remove(request.user)
            self.get_object().save()
            msg = {'success': 'You left from group.'}
            status_code = status.HTTP_200_OK
        else:
            msg = {'error': 'You are not member of this group.'}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=status_code)

    @detail_route(permission_classes=[IsMemberOrTeacherGroup])
    def invite(self, request, pk):
        nim = request.query_params.get('nim')
        if not nim:
            return Response(
                {'error': 'Please specify a valid nim in query params.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(nim=nim)
        except Student.DoesNotExist:
            student = None

        if not student:
            return Response(
                {'error': 'The student with that nim doesn\'t exist.'},
                status=status.HTTP_404_NOT_FOUND)

        if self.get_object().pendings.filter(
                student__pk=student.user.pk).exists():
            return Response(
                {'error': 'The student with that nim\
                 is in pending approval.'},
                status=status.HTTP_400_BAD_REQUEST)

        elif request.user.is_teacher():
            self.get_object().members.add(student.user)
            return Response({'success': 'User has been added to group.'},
                            status=status.HTTP_201_CREATED)

        elif self.get_object().members.filter(
                pk=student.user.pk).exists():
            return Response(
                {'error': 'The student with that nim already\
                 member in this group.'},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            PendingApproval.objects.create(
                student=student.user, group=self.get_object()
            )
            msg = {'success': 'Wait for approval.'}
            status_code = status.HTTP_200_OK
            return Response(msg, status=status_code)

    @detail_route(permission_classes=[IsTeacherGroup])
    def kick(self, request, pk):
        nim = request.query_params.get('nim')
        if not nim:
            return Response(
                {'error': 'Please specify a valid nim in query params.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(nim=nim)
        except Student.DoesNotExist:
            student = None

        if not student:
            return Response(
                {'error': 'The student with that nim doesn\'t exist.'},
                status=status.HTTP_404_NOT_FOUND)

        if student in self.get_object().members.all():
            self.get_object().members.remove(student)
            return Response(
                {'success': 'Member successfully removed.'}
            )
        else:
            return Response(
                {'error': 'The student with that nim' +
                          'isn\'t member of this group.'},
                status=status.HTTP_404_NOT_FOUND)


class PendingApprovalViewSet(BaseLoginRequired, ListModelMixin,
                             DestroyModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = PendingApproveSerializer
    filter_fields = ['student', ]

    def get_queryset(self):
        return PendingApproval.objects.filter(
            group__pk=self.kwargs.get('group_pk'))

    def get_permissions(self):
        self.permission_classes += (IsTeacherGroup,)
        return super(PendingApprovalViewSet, self).get_permissions()

    @detail_route(permission_classes=[IsTeacherGroup])
    def approve(self, request, group_pk, pk):
        self.get_object().approve()

        return Response({'success': 'User has been added to group.'},
                        status=status.HTTP_201_CREATED)

    @list_route(permission_classes=[IsTeacherGroup])
    def approve_all(self, request, group_pk):
        group = Group.objects.get(pk=group_pk)
        if self.get_queryset():
            users = User.objects.filter(
                pk__in=self.get_queryset().values_list('student', flat=True))
            group.members.add(*users)
            group.save()
            self.get_queryset().delete()

            msg = {'success': 'Users has been added to group.'}
            status_code = status.HTTP_201_CREATED
        else:
            msg = {'error': 'No join requests.'}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(msg, status=status_code)
