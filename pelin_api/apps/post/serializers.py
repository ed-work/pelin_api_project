from rest_framework import serializers
from apps.core.serializers import UserSerializer
from .models import Post, Comment


class GroupPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    votes_count = serializers.IntegerField(source='get_votes_count',
                                           required=False)

    class Meta:
        model = Post
        extra_kwargs = {
            'group': {'required': False},
            'votes': {'read_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        extra_kwargs = {
            'post': {'required': False, 'write_only': True},
            'user': {'required': False}
        }
