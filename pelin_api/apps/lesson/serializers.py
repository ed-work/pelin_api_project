from rest_framework import serializers
from .models import Lesson, LessonFiles


class LessonFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFiles
        fields = ('id', 'file')
        extra_kwargs = {
            'lesson': {'required': False}
        }


class LessonSerializer(serializers.ModelSerializer):
    files = LessonFilesSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Lesson
        extra_kwargs = {
            'group': {'required': False}
        }

    def create(self, validated_data):
        lesson = super(LessonSerializer, self).create(validated_data)

        if self.context['request'].FILES:
            try:
                files = self.context['request'].FILES.getlist('files')
                for f in files:
                    LessonFiles.objects.create(lesson=lesson, file=f)
            except Exception, e:
                print e

        return lesson
