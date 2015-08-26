from rest_framework import serializers, exceptions
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

    def get_major(self, obj):
        return obj.get_major_display()

    class Meta:
        model = Student
        fields = ('nim', 'major')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('nik', 'username')


class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    teacher = TeacherSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'write_only': True}
        }
