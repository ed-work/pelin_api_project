from django.conf.urls import url
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter

from .core import views as core_views
from .group import views as group_views
from .post import views as group_post_views
from .lesson import views as lesson_views
from .assignment import views as assignment_views
from .message import views as message_views
from .notif import views as notif_views
from .video import views as video_views

router = DefaultRouter(trailing_slash=False)
router.register(r'users', core_views.UserViewset)
router.register(r'groups', group_views.GroupViewSet)
router.register(r'public/groups', group_views.PublicGroupViewSet)
router.register(r'messages', message_views.ConversationViewSet,
                base_name='message')
router.register(r'notifications', notif_views.NotificationViewset,
                base_name='notification')
router.register(r'videos', video_views.VideoViewset, base_name='video')

pendings_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                     trailing_slash=False)
pendings_router.register(r'pendings', group_views.PendingApprovalViewSet,
                         base_name='pending')

members_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                    trailing_slash=False)
members_router.register(r'members', group_views.MemberListViewSet,
                        base_name='member')

group_post_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                       trailing_slash=False)
group_post_router.register(r'posts', group_post_views.GroupPostViewSet,
                           base_name='post')

group_postcomment_router = NestedSimpleRouter(group_post_router,
                                              r'posts', lookup='post',
                                              trailing_slash=False)
group_postcomment_router.register(r'comments', group_post_views.CommentViewSet,
                                  base_name='comment')

lesson_router = NestedSimpleRouter(router, r'groups', lookup='group',
                                   trailing_slash=False)
lesson_router.register(r'lessons', lesson_views.LessonViewSet,
                       base_name='lesson')
public_lesson_router = NestedSimpleRouter(router, r'public/groups',
                                          lookup='group', trailing_slash=False)
public_lesson_router.register(r'lessons', lesson_views.PublicLessonViewSet,
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
    url(r'^tokeninfo', 'rest_framework_jwt.views.verify_jwt_token',
        name='verify-token'),
    url(r'^my_assignments', assignment_views.MyAssignments.as_view(),
        name='get-my-assignments'),
]

urlpatterns += (
    router.urls +
    pendings_router.urls +
    members_router.urls +
    group_post_router.urls +
    group_postcomment_router.urls +
    lesson_router.urls +
    public_lesson_router.urls +
    assignment_router.urls
)
