from django.conf.urls import url
from core import views as core_views
from group import views as group_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register(r'users', core_views.UserViewset)
router.register(r'groups', group_views.GroupViewSet)


urlpatterns = [
    url(r'^jwt', 'rest_framework_jwt.views.obtain_jwt_token',
        name='obtain-jwt'),
    url(r'^auth', core_views.CustomObtainAuthToken.as_view(), name='obtain-token'),
]

urlpatterns += router.urls
