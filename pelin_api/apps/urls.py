from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^jwt', 'rest_framework_jwt.views.obtain_jwt_token',
        name='obtain-jwt'),
    url(r'^auth', views.CustomObtainAuthToken.as_view(), name='obtain-token'),
    url(r'^tes$', views.TesView.as_view())
]
