"""pelin_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'apps.video.views.index', name='home'),
    url(r'^search/$', 'apps.video.views.search', name='search'),
    url(r'^register/$', 'apps.core.views.register', name='register'),
    url(r'^forgot_password/$', 'apps.core.views.forgot_password',
        name='password-reset'),
    url(r'^forgot_password/confirm$',
        'apps.core.views.forgot_password_confirm',
        name='password-reset-confirm'),
    url(r'^kategori/(?P<category>.*)/$',
        'apps.video.views.kategori', name='category'),
    url(r'^materi/$', 'apps.group.views.materi', name='list-group'),
    url(r'^video/(?P<pk>.+)/$',
        'apps.video.views.video_detail',
        name='video-detail'),
    url(r'^materi/(?P<group_id>.+)/$',
        'apps.group.views.materi_group', name='list-group-lessons'),
    url(r'^kelas/$', 'apps.core.views.kelas', name='kelas'),
    url(r'^kelas/.*$', 'apps.core.views.kelas', name='kelas'),
    url(r'^api/', include('apps.urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
