from rest_framework import serializers
from . import models as group_models


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = group_models.Group
        extra_kwargs = {
            'members': { 'read_only': True, 'required': False },
            'teacher': { 'required': False }
        }