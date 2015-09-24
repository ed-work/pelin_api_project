from rest_framework import viewsets
from .serializers import AssignmentSerializer
from apps.core.views import BaseLoginRequired
from .models import Assignment


class AssignmentViewSet(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.filter(group__pk=self.kwargs.get('group_pk'))
