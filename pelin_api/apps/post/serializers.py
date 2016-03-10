from rest_framework import serializers
from rest_framework.reverse import reverse
from apps.core.serializers import UserSerializer
from .models import Post


class GroupPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    votes_count = serializers.IntegerField(source='get_votes_count')

    class Meta:
        model = Post
        extra_kwargs = {
            'group': {'required': False}
        }
