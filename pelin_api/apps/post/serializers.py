from rest_framework import serializers

from apps.core.mixins import RequestContextSerializer
from apps.core.serializers import UserSerializer
from .models import Post, Comment


class GroupPostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    me = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
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

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    def get_me(self, obj):
        return obj.user == self.context.get('request').user

    class Meta:
        model = Post
        extra_kwargs = {
            'group': {'required': False},
            'votes': {'read_only': True}
        }


class CommentSerializer(RequestContextSerializer, serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    me = serializers.SerializerMethodField()

    def get_user(self, obj):
        if obj.user.is_teacher():
            status = 'teacher'
        else:
            status = 'student'

        user_serializer = UserSerializer(
            obj.user,
            fields=['name', 'url', 'photo', status],
            context={'request': self.request})
        return user_serializer.data

    def get_me(self, obj):
        return obj.user == self.user

    class Meta:
        model = Comment
        extra_kwargs = {
            'post': {'required': False, 'write_only': True},
            'user': {'required': False}
        }
