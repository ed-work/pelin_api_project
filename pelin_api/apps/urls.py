from django.conf.urls import include, url


urlpatterns = [
    url(r'^auth$', 'rest_framework_jwt.views.obtain_jwt_token')
]
