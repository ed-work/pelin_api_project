from rest_framework import serializers
from .models import Post


class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
