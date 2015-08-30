from rest_framework import serializers
from . import models as group_models


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = group_models.Group