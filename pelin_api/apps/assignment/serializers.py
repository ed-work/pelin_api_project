from os.path import basename
import datetime

from rest_framework import serializers
from rest_framework.reverse import reverse
from apps.core.serializers import UserSerializer

from .models import Assignment, AssignmentFiles, SubmittedAssignment


class AssignmentFilesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return basename(obj.file.name)

    class Meta:
        model = AssignmentFiles
        fields = ('id', 'name', 'file')
        extra_kwargs = {
            'assignment': {'required': False}
        }


class AssignmentSerializer(serializers.ModelSerializer):
    is_submitted = serializers.SerializerMethodField()
    is_passed = serializers.SerializerMethodField()
    group_url = serializers.SerializerMethodField()
    files = AssignmentFilesSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Assignment
        extra_kwargs = {
            'group': {'required': False, 'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        super(AssignmentSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request').user.is_teacher():
            self.fields.pop('is_submitted')

    def get_group_url(self, obj):
        return reverse('api:group-detail', kwargs={'pk': obj.group.pk},
                       request=self.context.get('request'))

    def get_is_submitted(self, obj):
        try:
            assignment = SubmittedAssignment.objects.get(
                student=self.context.get('request').user, assignment=obj)
        except SubmittedAssignment.DoesNotExist:
            assignment = None

        if assignment:
            return True
        return False

    def get_is_passed(self, obj):
        return datetime.datetime.now() > obj.due_date.replace(tzinfo=None)


class SubmittedAssignmentFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.FileField(source='file')

    def get_name(self, obj):
        return basename(obj.file.name)

    class Meta:
        model = SubmittedAssignment
        fields = ('url', 'name')


class SubmittedAssignmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(
        fields=('id', 'first_name', 'last_name', 'student', 'url'))
    assignment_url = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(SubmittedAssignmentSerializer, self).__init__(*args, **kwargs)
        if not self.context.get('request').user.is_teacher():
            self.fields.pop('student')

    def get_file(self, obj):
        serializer = SubmittedAssignmentFileSerializer(obj, context={
            'request': self.context.get('request')})
        return serializer.data

    def get_assignment_url(self, obj):
        return reverse('api:assignment-detail',
                       kwargs={
                           'pk': obj.assignment.pk,
                           'group_pk': obj.assignment.group.pk
                       },
                       request=self.context.get('request', None))

    class Meta:
        model = SubmittedAssignment
        extra_kwargs = {
            'assignment': {'required': False},
            'student': {'required': False}
        }
