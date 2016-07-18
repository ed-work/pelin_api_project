import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404, ListAPIView

from rest_framework.response import Response

from apps.core.views import BaseLoginRequired
from apps.group.models import Group
from .permissions import AssignmentPermission
from .serializers import AssignmentSerializer, SubmittedAssignmentSerializer
from .models import Assignment, SubmittedAssignment


class AssignmentViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    filter_fields = ['id', 'group', 'due_date']

    def get_permissions(self):
        self.permission_classes += (AssignmentPermission,)
        return super(AssignmentViewSet, self).get_permissions()

    def get_queryset(self):
        assignments = Assignment.objects.filter(
            group__pk=self.kwargs.get('group_pk'))\
            .order_by('-created_at', '-due_date')\
            .select_related('group')
        return assignments

    def perform_create(self, serializer):
        group = get_object_or_404(Group, pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)

    @detail_route(methods=['post'])
    def submit(self, request, group_pk, pk):
        if request.user.is_teacher():
            return Response({'detail': 'You are not student.'},
                            status=status.HTTP_403_FORBIDDEN)

        assignment = get_object_or_404(Assignment, pk=pk)

        if datetime.datetime.now() < assignment.due_date.replace(tzinfo=None):
            try:
                submitted_assignment = SubmittedAssignment.objects.get(
                    assignment=assignment, user=request.user)
            except SubmittedAssignment.DoesNotExist:
                submitted_assignment = None

            if submitted_assignment:
                serializer = SubmittedAssignmentSerializer(
                    submitted_assignment, data=request.data, partial=True,
                    context={'request': request})
            else:
                serializer = SubmittedAssignmentSerializer(
                    data=request.data, context={'request': request})

            if serializer.is_valid(raise_exception=True):
                serializer.save(assignment=assignment, user=request.user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'The assignment has passed deadline.'},
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['GET'])
    def submitted(self, request, group_pk, pk):
        if request.user.is_teacher():
            submitted_assignments = SubmittedAssignment.objects.filter(
                assignment__pk=pk)
            serializer = SubmittedAssignmentSerializer(
                submitted_assignments, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            try:
                submitted_assignment = SubmittedAssignment.objects.get(
                    assignment__pk=pk, user=request.user)
                serializer = SubmittedAssignmentSerializer(
                    submitted_assignment, context={'request': request})
                return Response(serializer.data)
            except SubmittedAssignment.DoesNotExist:
                return Response(
                    {'detail': 'You have not submitted to this assignment.'},
                    status=status.HTTP_400_BAD_REQUEST)


class MyAssignments(BaseLoginRequired, ListAPIView):
    def list(self, request, *args, **kwargs):
        group_ids = request.user.group_members.values_list('id', flat=True)
        assignments = Assignment.objects.filter(
            group__pk__in=group_ids, due_date__gt=datetime.datetime.now())\
            .select_related('group')

        if 'count' in request.query_params:
            count = assignments.exclude(submittedassignment__user=request.user)
            return Response({'count': count.count()})

        serializer = AssignmentSerializer(assignments, many=True, group=True,
                                          context={'request': request})

        return Response(serializer.data)
