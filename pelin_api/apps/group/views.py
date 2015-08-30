from rest_framework import viewsets
from . import serializers as group_serializers
from . import models as group_models


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = group_serializers.GroupSerializer
    queryset = group_models.Group.objects.all()