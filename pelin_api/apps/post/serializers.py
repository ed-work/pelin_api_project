from rest_framework import serializers
from rest_framework.reverse import reverse
from apps.core.serializers import UserSerializer
from .models import Post


class GroupPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    url = serializers.SerializerMethodField()
    group_url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('api:post-detail',
                       kwargs={'pk': obj.pk, 'group_pk': obj.group.pk},
                       request=self.context.get('request'))

    def get_group_url(self, obj):
        return reverse('api:group-detail', kwargs={'pk': obj.group.pk},
                       request=self.context.get('request'))

    class Meta:
        model = Post
        extra_kwargs = {
            'group': {'required': False}
        }
