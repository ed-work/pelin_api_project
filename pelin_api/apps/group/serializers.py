from rest_framework import serializers
from rest_framework.reverse import reverse

from . import models as group_models


class GroupSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('api:group-detail', kwargs={'pk': obj.pk},
                       request=self.context.get('request'))

    class Meta:
        model = group_models.Group
        extra_kwargs = {
            'members': {'read_only': True, 'required': False},
            'teacher': {'required': False}
        }
