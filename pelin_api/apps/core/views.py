from rest_framework import views, parsers, renderers, permissions, \
    authentication, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from . import serializers
from . import permissions as perm
from .models import User


class CustomObtainAuthToken(views.APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser
    )
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = serializers.CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': unicode(token.key),
        }

        return Response(content)


class BaseLoginRequired(object):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)


class UserViewset(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (perm.CreateUserPermission,)
        else:
            self.permission_classes += (perm.CustomUserPermission,)
        return super(UserViewset, self).get_permissions()

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            request = self.initialize_request(request, *args, **kwargs)
            if request.user.is_authenticated():
                kwargs['pk'] = request.user.pk

        return super(UserViewset, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.NewUserSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        new_user = User.objects.get(
            email=serializer.validated_data.get('email'))
        new_user_serialized = serializers.UserSerializer(new_user)

        return Response(new_user_serialized.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
