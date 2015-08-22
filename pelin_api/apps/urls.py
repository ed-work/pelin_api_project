from django.conf.urls import include, url
from core import views

urlpatterns = [
    url(r'^jwt', 'rest_framework_jwt.views.obtain_jwt_token',
        name='obtain-jwt'),
    url(r'^auth', views.CustomObtainAuthToken.as_view(), name='obtain-token')
]
