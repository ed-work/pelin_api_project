from django.shortcuts import render
from django.db.models import Q
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
    queryset = Video.objects.select_related('user')
    filter_fields = ['category']

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAuthenticated, VideoPermission)
        return super(VideoViewset, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if 'mine' in self.request.query_params:
            return self.queryset.filter(user=self.request.user)

        if 'search' in self.request.query_params:
            keyword = self.request.query_params.get('search')
            return self.queryset.filter(
                Q(title__icontains=keyword) |
                Q(user__name__icontains=keyword) |
                Q(category__name__in=[keyword]))\
                .prefetch_related('category').distinct()

        return super(VideoViewset, self).get_queryset()


def index(request):
    videos = Video.objects\
        .select_related('user')\
        .prefetch_related('category')
    return render(request, 'index.html', {'videos': videos})


def search(request):
    try:
        keyword = request.GET.get('q')
        videos = Video.objects.filter(
            Q(title__icontains=keyword) |
            Q(user__name__icontains=keyword) |
            Q(category__name__in=[keyword]))\
            .prefetch_related('category').distinct()
    except:
        keyword = ''
        videos = None
    return render(request, 'search.html', {
        'keyword': keyword,
        'videos': videos
    })


def kategori(request, category):
    videos = Video.objects\
        .filter(category__name__in=[category])\
        .prefetch_related('category')
    return render(request, 'kategori.html', {
        'videos': videos, 'category': category
    })


def video_detail(request, pk):
    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotFound:
        video = None

    return render(request, 'video_detail.html', {'video': video})
