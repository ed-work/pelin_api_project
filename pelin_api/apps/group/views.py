from apps.core.functions import get_object_or_none
from apps.core.models import Student, User
from apps.core.serializers import UserSerializer
from apps.core.views import BaseLoginRequired
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.mixins import (DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Group, PendingApproval
from .permissions import (GroupPermission, IsMemberOrTeacherGroup, IsStudent,
                          IsTeacherGroup)
from .serializers import GroupSerializer, PendingApproveSerializer


class GroupViewSet(BaseLoginRequired, ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects\
        .select_related('teacher')\
        .select_related('teacher__teacher')\
        .prefetch_related('members')\
        .prefetch_related('pendings')
    filter_fields = ['id', 'teacher', 'members', 'title']

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_permissions(self):
        self.permission_classes += (GroupPermission,)
        return super(GroupViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_teacher():
            return self.queryset.filter(teacher=self.request.user)
        return super(GroupViewSet, self).get_queryset()

    @detail_route(permission_classes=[permissions.IsAuthenticated, IsStudent])
    def join(self, request, pk=None):
        user = request.user
        obj = self.get_object()

        if obj.pendings.filter(
                user__pk=user.pk).exists():
            msg = {'detail': 'Your join request in this group is pending.'}
            status_code = status.HTTP_400_BAD_REQUEST
        elif obj.members.filter(pk=user.pk).exists():
            msg = {'detail': 'You are member in this group.'}
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            PendingApproval.objects.create(
                user=user, group=self.get_object()
            )
            msg = {'detail': 'Wait for approval.'}
            status_code = status.HTTP_200_OK
        return Response(msg, status=status_code)

    @detail_route(permission_classes=[IsStudent])
    def leave(self, request, pk=None):
        user = request.user
        obj = self.get_object()

        if obj.members.filter(pk=user.pk).exists():
            obj.members.remove(user)
            obj.save()
            msg = {'success': 'You left from group.'}
            status_code = status.HTTP_200_OK
        else:
            msg = {'error': 'You are not member of this group.'}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=status_code)

    @detail_route(permission_classes=[IsStudent])
    def cancel(self, request, pk=None):
        user = request.user
        pending = get_object_or_none(PendingApproval,
                                     user__id=user.id,
                                     group__id=pk)

        if pending:
            pending.delete()
            msg = {'detail': 'You cancelled join request.'}
            status_code = status.HTTP_200_OK
        else:
            msg = {'detail': 'You are not joining this group.'}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(msg, status=status_code)


class PendingApprovalViewSet(BaseLoginRequired, ListModelMixin,
                             DestroyModelMixin, GenericViewSet):
    serializer_class = PendingApproveSerializer
    filter_fields = ['student', ]

    def get_queryset(self):
        return PendingApproval.objects.filter(
            group__pk=self.kwargs.get('group_pk'))

    def get_permissions(self):
        self.permission_classes += (IsTeacherGroup,)
        return super(PendingApprovalViewSet, self).get_permissions()

    @detail_route(permission_classes=[IsTeacherGroup])
    def approve(self, request=None, group_pk=None, pk=None):
        self.get_object().approve()
        return Response({'success': 'User has been added to group.'},
                        status=status.HTTP_201_CREATED)

    @list_route(permission_classes=[IsTeacherGroup])
    def approve_all(self, request, group_pk):
        if self.get_queryset():
            group = Group.objects.get(pk=group_pk)
            users = User.objects.filter(
                pk__in=self.get_queryset().values_list('user', flat=True))
            group.members.add(*users)
            group.save()
            self.get_queryset().delete()

            msg = {'success': 'Users has been added to group.'}
            status_code = status.HTTP_201_CREATED
        else:
            msg = {'error': 'No join requests.'}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(msg, status=status_code)

    @detail_route(permission_classes=[IsTeacherGroup])
    def decline(self, request, group_pk, pk):
        self.get_object().delete()
        return Response({'detail': 'User has been declined.'},
                        status=status.HTTP_200_OK)


class MemberListViewSet(BaseLoginRequired, ListAPIView,
                        GenericViewSet):
    serializer_class = UserSerializer

    @list_route(permission_classes=[IsMemberOrTeacherGroup])
    def invite(self, request, group_pk=None):
        nim = self.request.query_params.get('nim')
        student = get_object_or_none(Student, nim=nim)

        return self.check_nim_exist(nim) or \
            self.check_student_exist(student) or \
            self.check_student_group(request, student) or \
            self.add_or_pending(request, student)

    @list_route(permission_classes=[IsTeacherGroup])
    def kick(self, request, group_pk=None):
        nim = self.request.query_params.get('nim')
        student = get_object_or_none(Student, nim=nim)

        return self.check_nim_exist(nim) or\
            self.check_student_exist(student) or\
            self.kick_student(student)

    def get_queryset(self):
        group = self.get_group()
        return group.members.select_related('student')

    def get_permissions(self):
        self.permission_classes += (GroupPermission,)
        return super(MemberListViewSet, self).get_permissions()

    def check_nim_exist(self, nim):
        if not nim:
            return Response(
                {'error': 'Please specify a valid nim in query params.'},
                status=status.HTTP_400_BAD_REQUEST)

    def check_student_exist(self, student):
        if not student:
            return Response(
                {'error': 'Student not found.'},
                status=status.HTTP_404_NOT_FOUND)

    def get_group(self):
        return get_object_or_404(Group, pk=self.kwargs.get('group_pk'))

    def check_student_group(self, request, student):
        group = self.get_group()
        if student.user in group.members.all():
            return Response(
                {'error': 'Already member in this group.'},
                status=status.HTTP_400_BAD_REQUEST)

        if group.pendings.filter(user__pk=student.user.pk).exists():
            if request.user.is_teacher():
                self.get_group().members.add(student.user)
                group.pendings.get(user_id=student.user.pk).delete()
                return Response({'success': 'User has been added to group.'},
                                status=status.HTTP_201_CREATED)
            return Response(
                {'error': 'Student in pending approval.'},
                status=status.HTTP_400_BAD_REQUEST)

    def add_or_pending(self, request, student):
        if request.user.is_teacher():
            self.get_group().members.add(student.user)
            return Response({'success': 'User has been added to group.'},
                            status=status.HTTP_201_CREATED)

        else:
            PendingApproval.objects.create(
                user=student.user, group=self.get_group()
            )
            msg = {'success': 'Wait for approval.'}
            status_code = status.HTTP_200_OK
            return Response(msg, status=status_code)

    def kick_student(self, student):
        if student.user in self.get_group().members.all():
            self.get_group().members.remove(student.user)
            return Response(
                {'success': 'Member successfully removed.'}
            )
        else:
            return Response(
                {'error': 'Student is not member of this group.'},
                status=status.HTTP_404_NOT_FOUND)


def materi(request):
    groups = Group.objects.all()
    return render(request, 'materi.html', {'groups': groups})


def materi_group(request, group_id):
    g = get_object_or_none(Group, pk=group_id)

    if not g:
        return HttpResponseRedirect('/materi')

    lessons = g.lesson_set.select_related('group')\
        .prefetch_related('files').all()

    return render(request, 'materi_group.html',
                  {'lessons': lessons, 'g': g})


class PublicGroupViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects\
        .select_related('teacher')\
        .select_related('teacher__teacher')\
        .prefetch_related('members')\
        .prefetch_related('pendings')
    filter_fields = ['id', 'teacher', 'members', 'title']
