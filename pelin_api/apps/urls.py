from django.conf.urls import url
from core import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewset)


urlpatterns = [
    url(r'^jwt', 'rest_framework_jwt.views.obtain_jwt_token',
        name='obtain-jwt'),
    url(r'^auth', views.CustomObtainAuthToken.as_view(), name='obtain-token'),
]

urlpatterns += router.urls