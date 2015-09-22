from django.conf.urls import url
from .core import views as core_views
from .group import views as group_views
from .post import views as group_post_views
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'users', core_views.UserViewset)
router.register(r'groups', group_views.GroupViewSet)

pendings_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                     trailing_slash=False)
pendings_router.register(r'pendings', group_views.PendingApprovalViewSet,
                         base_name='pendings')

group_post_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                       trailing_slash=False)
group_post_router.register(r'posts', group_post_views.GroupPostViewSet,
                           base_name='posts')

urlpatterns = [
    url(r'^jwt', 'rest_framework_jwt.views.obtain_jwt_token',
        name='obtain-jwt'),
    url(r'^auth', core_views.CustomObtainAuthToken.as_view(),
        name='obtain-token'),
]

urlpatterns += (
    router.urls +
    pendings_router.urls +
    group_post_router.urls
)
