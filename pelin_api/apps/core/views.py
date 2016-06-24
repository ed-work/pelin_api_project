from uuid import uuid4
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render
from django.contrib import messages
from shortid import ShortId
from rest_framework import views, parsers, renderers, permissions, \
    viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from . import serializers
from . import permissions as perm
from apps.group.serializers import GroupSerializer
from .models import User, Student, UserPasswordReset
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


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
    # authentication_classes = (authentication.TokenAuthentication,)
    authentication_classes = (JSONWebTokenAuthentication,)


class UserViewset(BaseLoginRequired, viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False) \
        .select_related('student', 'teacher')
    filter_fields = ['id', 'student', 'teacher', 'email', 'status']

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
        return serializers.NewUserSerializer \
            if self.request.method == 'POST' else self.serializer_class

    def get_object(self):
        obj = User.objects.get_with(self.kwargs.get('pk'))
        if not obj:
            return super(UserViewset, self).get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        new_user = User.objects.get(
            email=serializer.validated_data.get('email'))
        new_user_serialized = serializers.UserSerializer(new_user, context={
            'request': self.request})

        return Response(new_user_serialized.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    @detail_route(methods=['GET'],
                  permission_classes=(permissions.IsAuthenticated,))
    def groups(self, request, pk=None):
        user = self.get_object()
        if user.is_teacher():
            joined_groups = user.group_teacher.all()
        else:
            joined_groups = user.group_members.all()

        serializer = GroupSerializer(joined_groups, many=True,
                                     context={'request': request})
        return Response(serializer.data)


def register(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        name = request.POST.get('name')
        nim = request.POST.get('nim')
        email = request.POST.get('email')
        major = request.POST.get('major')

        try:
            u = User.objects.create(email=email, name=name)
            u.set_password(password)
            u.save()

            s = Student.objects.create(user=u, nim=nim, major=major)
            s.save()
            messages.info(
                request,
                "Register berhasil, silahkan login")
        except Exception, e:
            messages.error(
                request,
                "Error! mohon cek kembali")
            print 'error register'
            print e

    return render(request, 'register.html')


def password_reset(request):
    if request.method == 'POST':
        nim = request.POST.get('nim')
        email = request.POST.get('email')

        try:
            u = Student.objects.select_related('user').\
                get(nim=nim, user__email=email).user
        except User.DoesNotExist:
            u = None

        if u:
            new_pass = ShortId().generate()
            confirm_code = str(uuid4())

            try:
                up = UserPasswordReset.objects.get(user=u)
            except:
                up = UserPasswordReset(user=u)

            up.code = confirm_code
            up.new_pass = new_pass
            up.save()

            subject = 'Password reset'
            to = [u.email]
            from_email = 'pelin.stmikbumogra@gmail.com'
            context = {'nim': u.student.nim,
                       'confirm_code': confirm_code,
                       'new_pass': new_pass}
            msg = get_template('password_reset_email.html').render(
                Context(context))

            mail = EmailMessage(subject, msg, to=to, from_email=from_email)
            mail.content_subtype = 'html'
            mail.send()
            success = 'success'
            error = None
        else:
            error = 'no user'
            success = None
    else:
        success = None
        error = None

    return render(request, 'password_reset.html',
                  {'success': success, 'error': error})


def password_reset_confirm(request):
    if 'code' in request.GET:
        code = request.GET.get('code')

        try:
            u = UserPasswordReset.objects.get(code=code)
            user = u.user
            user.set_password(u.new_pass)
            user.save()
            u.delete()
            success = 'success'
        except UserPasswordReset.DoesNotExist:
            code = None
            success = None
    else:
        code = None
        success = None

    return render(request,
                  'password_reset_confirm.html',
                  {'code': code, 'success': success})
