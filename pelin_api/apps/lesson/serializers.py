from rest_framework import serializers
from .models import Lesson, LessonFiles


class LessonFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFiles


class LessonSerializer(serializers.ModelSerializer):
    files = LessonFilesSerializer()

    class Meta:
        model = Lesson
