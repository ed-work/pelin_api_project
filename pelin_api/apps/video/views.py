from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import VideoSerializer
from .permissions import VideoPermission
from .models import Video


class VideoViewset(ModelViewSet):
    serializer_class = VideoSerializer
    psermission_classes = (VideoPermission,)

    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Video.objects.all()

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAuthenticated, VideoPermission)
        return super(VideoViewset, self).get_permissions()


def index(request):
    return render('index.html', {'tes': 'tes'})
