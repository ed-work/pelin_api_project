from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.core.views import BaseLoginRequired

from .serializers import NotificationSerializer


class NotificationViewset(
        BaseLoginRequired,
        ListModelMixin,
        GenericViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.request.user.notifications.all()

    @list_route(methods=['GET'],
                permission_classes=[permissions.IsAuthenticated])
    def mark_read(self, request):
        self.request.user.notifications.mark_all_as_read()
        return Response({'status': 'success'})

    @list_route(methods=['GET'],
                permission_classes=[permissions.IsAuthenticated])
    def clear(self, request):
        self.request.user.notifications.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
