from os.path import basename

from rest_framework import serializers
from rest_framework.reverse import reverse

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

        if assignment: return True
        return False


class SubmittedAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedAssignment
        extra_kwargs = {
            'assignment': {'required': False, 'write_only': True},
            'student': {'required': False}
        }
