from os.path import basename
import datetime

from rest_framework import serializers
from rest_framework.reverse import reverse
from apps.core.serializers import UserSerializer
from apps.group.serializers import GroupSerializer

from .models import Assignment, SubmittedAssignment


# class AssignmentFilesSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()

#     def get_name(self, obj):
#         return basename(obj.file.name)

#     class Meta:
#         model = AssignmentFiles
#         fields = ('id', 'name', 'file')
#         extra_kwargs = {
#             'assignment': {'required': False}
#         }


class AssignmentSerializer(serializers.ModelSerializer):
    is_submitted = serializers.SerializerMethodField()
    is_passed = serializers.SerializerMethodField()
    group_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    # files = AssignmentFilesSerializer(
    #     required=False, read_only=True, many=True)

    class Meta:
        model = Assignment
        extra_kwargs = {
            'group': {'required': False}
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(AssignmentSerializer, self).__init__(*args, **kwargs)
        # print self.fields.get('group')
        if group:
            self.fields['group'] = GroupSerializer(fields=('id', 'title'))

        if self.context.get('request').user.is_teacher():
            self.fields.pop('is_submitted')

    def get_group_url(self, obj):
        return reverse('api:group-detail', kwargs={'pk': obj.group.pk},
                       request=self.context.get('request'))

    def get_url(self, obj):
        return reverse('api:assignment-detail',
                       kwargs={
                           'pk': obj.pk,
                           'group_pk': obj.group.pk
                       },
                       request=self.context.get('request', None))

    def get_is_submitted(self, obj):
        try:
            assignment = SubmittedAssignment.objects.get(
                user=self.context.get('request').user, assignment=obj)
        except SubmittedAssignment.DoesNotExist:
            assignment = None

        if assignment:
            return True
        return False

    def get_is_passed(self, obj):
        return datetime.datetime.now() > obj.due_date.replace(tzinfo=None)

    # def create(self, validated_data):
    #     assignment = super(AssignmentSerializer, self).create(validated_data)

    #     if self.context['request'].FILES:
    #         try:
    #             files = self.context['request'].FILES.getlist('files')
    #             for f in files:
    #                 AssignmentFiles.objects.create(
    #                     assignment=assignment, file=f)
    #         except Exception as e:
    #             print e

    #     return assignment


class SubmittedAssignmentFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.FileField(source='file')

    def get_name(self, obj):
        return basename(obj.file.name)

    class Meta:
        model = SubmittedAssignment
        fields = ('url', 'name')


class SubmittedAssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        fields=('id', 'first_name', 'name', 'student', 'url'))
    assignment_url = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(SubmittedAssignmentSerializer, self).__init__(*args, **kwargs)
        if not self.context.get('request').user.is_teacher():
            self.fields.pop('user')

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
            'user': {'required': False}
        }
