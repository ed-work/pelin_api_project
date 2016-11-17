from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Group, PendingApproval
from apps.core.serializers import UserSerializer
from apps.core.mixins import DynamicFieldsSerializer


class GroupSerializer(DynamicFieldsSerializer, serializers.ModelSerializer):
    teacher = UserSerializer(required=False, remove_fields=['student'])
    is_owner = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()
    is_pending = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    # semester = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context.get('request').user.id == obj.teacher_id

    def get_url(self, obj):
        return reverse('api:group-detail', kwargs={'pk': obj.pk},
                       request=self.context.get('request'))

    def get_is_joined(self, obj):
        return self.context['request'].user in obj.members.all()

    def get_is_pending(self, obj):
        return obj.pendings.filter(
            user__pk=self.context['request'].user.pk).exists()

    def get_members(self, obj):
        return obj.members.count()

    # def get_semester(self, obj):
    #     return obj.get_semester_display()

    class Meta:
        model = Group
        extra_kwargs = {
            'members': {'read_only': True, 'required': False},
            'teacher': {'required': False}
        }


class PendingApproveSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PendingApproval
        fields = ('id', 'user')
