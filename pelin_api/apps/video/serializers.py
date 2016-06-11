from rest_framework.serializers import ModelSerializer
from apps.core.serializers import UserSerializer
from .models import Video


class VideoSerializer(ModelSerializer):
    user = UserSerializer(fields=['id', 'name', 'teacher'], required=False)

    class Meta:
        model = Video
        extra_kwargs = {
            'user': {'required': False, 'read_only': True}
        }
