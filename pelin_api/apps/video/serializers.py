from rest_framework.serializers import ModelSerializer
from taggit_serializer.serializers import (
    TaggitSerializer, TagListSerializerField
)
from apps.core.serializers import UserSerializer
from .models import Video


class VideoSerializer(TaggitSerializer, ModelSerializer):
    user = UserSerializer(fields=['id', 'name', 'teacher'], required=False)
    category = TagListSerializerField()

    class Meta:
        model = Video
        extra_kwargs = {
            'user': {'required': False, 'read_only': True}
        }
