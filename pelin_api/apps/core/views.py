from rest_framework import views, parsers, renderers, permissions, \
    authentication, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import serializers
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
        serializer = serializers.CustomAuthTokenSerialzer(data=request.data)
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