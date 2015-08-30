from rest_framework import viewsets
from . import serializers as group_serializers
from . import models as group_models
from apps.core import views as core_views


class GroupViewSet(core_views.BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = group_serializers.GroupSerializer
    queryset = group_models.Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)