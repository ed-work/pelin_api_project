from rest_framework import viewsets

from apps.group.models import Group
from .serializers import AssignmentSerializer
from apps.core.views import BaseLoginRequired
from .models import Assignment


class AssignmentViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.filter(group__pk=self.kwargs.get('group_pk'))

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group_pk'))
        serializer.save(group=group)
