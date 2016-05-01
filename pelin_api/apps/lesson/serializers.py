from os.path import basename

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Lesson, LessonFiles


class LessonFilesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return basename(obj.file.name)

    class Meta:
        model = LessonFiles
        fields = ('id', 'name', 'file')
        extra_kwargs = {
            'lesson': {'required': False}
        }


class LessonSerializer(serializers.ModelSerializer):
    group_url = serializers.SerializerMethodField()
    files = LessonFilesSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Lesson
        extra_kwargs = {
            'group': {'required': False, 'write_only': True}
        }

    def get_group_url(self, obj):
        return reverse('api:group-detail', kwargs={'pk': obj.group.pk},
                       request=self.context.get('request'))

    def create(self, validated_data):
        lesson = super(LessonSerializer, self).create(validated_data)

        if self.context['request'].FILES:
            try:
                files = self.context['request'].FILES.getlist('files')
                for f in files:
                    LessonFiles.objects.create(lesson=lesson, file=f)
            except Exception as e:
                print e

        return lesson
