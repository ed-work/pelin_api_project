from rest_framework import views, parsers, renderers, permissions, \
    authentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import CustomAuthTokenSerialzer


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
        serializer = CustomAuthTokenSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': unicode(token.key),
        }

        return Response(content)


class TesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        return Response({
            'wew': 'wooooooowwww'
        })
