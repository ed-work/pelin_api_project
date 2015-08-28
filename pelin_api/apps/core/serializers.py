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
    # nim = serializers.CharField()
    student = StudentSerializer(required=False)
    teacher = TeacherSerializer(required=False)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = User
        fields = ('id', 'student', 'teacher', 'status', 'last_login', 'email',
                  'first_name', 'last_name', 'date_joined', 'is_active',
                  'photo')
        extra_kwargs = {
            'password': {'write_only': True},
            # 'nim': {'write_only': True}
        }


class NewUserSerializer(serializers.Serializer):
    nim = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    photo = serializers.ImageField(required=False)

    def create(self, validated_data):
        usr = User(email=validated_data.get('email'),
                   first_name=validated_data.get('first_name'),
                   last_name=validated_data.get('last_name'))

        usr.set_password(validated_data.get('password'))
        usr.save()

        student = Student(user=usr, nim=validated_data.get('nim'))
        student.save()

        return usr

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.set_password(validated_data.get('password'))
        instance.save()

        return instance
