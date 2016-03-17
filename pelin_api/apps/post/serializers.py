from rest_framework import serializers
from apps.core.serializers import UserSerializer
from .models import Post, Comment


class GroupPostSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=False)
    user = serializers.SerializerMethodField()
    votes_count = serializers.IntegerField(source='get_votes_count',
                                           required=False)

    def get_user(self, obj):
        if obj.user.is_teacher():
            status = 'teacher'
        else:
            status = 'student'
        user_serializer = UserSerializer(
            obj.user,
            fields=['name', 'url', 'photo', status],
            context={'request': self.context.get('request')})
        return user_serializer.data

    class Meta:
        model = Post
        extra_kwargs = {
            'group': {'required': False},
            'votes': {'read_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if obj.user.is_teacher():
            status = 'teacher'
        else:
            status = 'student'

        user_serializer = UserSerializer(
            obj.user,
            fields=['name', 'url', 'photo', status],
            context={'request': self.context.get('request')})
        return user_serializer.data

    class Meta:
        model = Comment
        extra_kwargs = {
            'post': {'required': False, 'write_only': True},
            'user': {'required': False}
        }
