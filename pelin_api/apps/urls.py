from django.conf.urls import url
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter

from .core import views as core_views
from .group import views as group_views
from .post import views as group_post_views
from .lesson import views as lesson_views
from .assignment import views as assignment_views
from .message import views as message_views

router = DefaultRouter(trailing_slash=False)
router.register(r'users', core_views.UserViewset)
router.register(r'groups', group_views.GroupViewSet)
router.register(r'messages', message_views.ConversationViewSet,
                base_name='message')

pendings_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                     trailing_slash=False)
pendings_router.register(r'pendings', group_views.PendingApprovalViewSet,
                         base_name='pending')

group_post_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                       trailing_slash=False)
group_post_router.register(r'posts', group_post_views.GroupPostViewSet,
                           base_name='post')

lesson_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                   trailing_slash=False)
lesson_router.register(r'lessons', lesson_views.LessonViewSet,
                       base_name='lesson')

assignment_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                       trailing_slash=False)
assignment_router.register(r'assignments', assignment_views.AssignmentViewSet,
                           base_name='assignment')

urlpatterns = [
    url(r'^jwt', 'rest_framework_jwt.views.obtain_jwt_token',
        name='obtain-jwt'),
    url(r'^auth', core_views.CustomObtainAuthToken.as_view(),
        name='obtain-token'),
]

urlpatterns += (
    router.urls +
    pendings_router.urls +
    group_post_router.urls +
    lesson_router.urls +
    assignment_router.urls
)
