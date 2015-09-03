from rest_framework import serializers, exceptions
from rest_framework.reverse import reverse
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from .models import User, Student, Teacher


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class StudentSerializer(serializers.ModelSerializer):
    major = serializers.SerializerMethodField()

    @staticmethod
    def get_major(obj):
        return obj.get_major_display()

    class Meta:
        model = Student
        fields = ('nim', 'major')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('nik', 'username')


class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)
    teacher = TeacherSerializer(required=False)

    status = serializers.SerializerMethodField()
    is_teacher = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    @staticmethod
    def get_status(obj):
        return obj.get_status_display()

    @staticmethod
    def get_is_teacher(obj):
        return obj.is_teacher()

    def get_url(self, obj):
        return reverse('api:user-detail', kwargs={'pk': obj.pk},
                       request=self.context.get('request'))

    class Meta:
        model = User
        fields = ('id', 'student', 'teacher', 'status', 'last_login', 'email',
                  'first_name', 'last_name', 'date_joined', 'is_active',
                  'is_teacher', 'url', 'photo')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class NewUserSerializer(serializers.Serializer):
    nim = serializers.CharField(write_only=True, required=False)
    nik = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)

    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    photo = serializers.ImageField(required=False, write_only=True)

    def create(self, validated_data):
        usr = User(email=validated_data.get('email'),
                   first_name=validated_data.get('first_name'),
                   last_name=validated_data.get('last_name'))

        usr.set_password(validated_data.get('password'))
        usr.save()

        if validated_data.get('username') and validated_data.get('nik'):
            usr.status = 1
            usr.save()
            Teacher.objects.create(user=usr, nik=validated_data.get('nik'),
                                   username=validated_data.get('username'))
        else:
            Student.objects.create(user=usr, nim=validated_data.get('nim'))

        return usr

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.set_password(validated_data.get('password'))
        instance.save()

        return instance

    def validate(self, attrs):
        if attrs.get('nim') and (attrs.get('username') or attrs.get('nik')):
            raise serializers.ValidationError('Choose one of nim and username')

        if (not attrs.get('nim')) and (not attrs.get('username')):
            raise serializers.ValidationError('Must have a valid nim/username')

        if attrs.get('username') and not attrs.get('nik'):
            raise serializers.ValidationError('Teacher must have a valid nik')

        return attrs