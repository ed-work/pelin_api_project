import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response

from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from apps.group.permissions import IsMemberOrTeacher
from .permissions import AssignmentPermission
from .serializers import AssignmentSerializer, SubmittedAssignmentSerializer
from .models import Assignment


class AssignmentViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        self.permission_classes += (IsMemberOrTeacher, AssignmentPermission)
        return super(AssignmentViewSet, self).get_permissions()

    def get_queryset(self):
        assignments = Assignment.objects.filter(
            group__pk=self.kwargs.get('group_pk'))
        if not self.request.user.is_teacher():
            return assignments.filter(due_date__gt=datetime.datetime.now())
        return assignments

    def perform_create(self, serializer):
        group = get_object_or_404(Group, pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)

    @detail_route(methods=['post'])
    def submit(self, request, group_pk, pk):
        if request.user.is_teacher():
            return Response({'detail': 'You are not student.'},
                            status=status.HTTP_403_FORBIDDEN)

        assignment = get_object_or_404(Assignment, pk=pk,
                                       due_date__gt=datetime.datetime.now())

        if datetime.datetime.now() < assignment.due_date.now():
            serializer = SubmittedAssignmentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(assignment=assignment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'The assignment has passed deadline.'},
                            status=status.HTTP_403_FORBIDDEN)
