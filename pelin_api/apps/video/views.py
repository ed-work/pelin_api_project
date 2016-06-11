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
    filter_fields = ['category']

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAuthenticated, VideoPermission)
        return super(VideoViewset, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def index(request):
    videos = Video.objects.all()
    return render(request, 'index.html', {'videos': videos})
