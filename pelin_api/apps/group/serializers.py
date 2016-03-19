from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Group, PendingApproval
from apps.core.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(required=False, remove_fields=['student'])
    url = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()
    pending_approve = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('api:group-detail', kwargs={'pk': obj.pk},
                       request=self.context.get('request'))

    def get_is_joined(self, obj):
        return self.context['request'].user in obj.members.all()

    def get_pending_approve(self, obj):
        return self.context['request'].user in obj.pendings.all()

    def get_members(self, obj):
        return obj.members.count()

    class Meta:
        model = Group
        extra_kwargs = {
            'members': {'read_only': True, 'required': False},
            'teacher': {'required': False}
        }


class PendingApproveSerializer(serializers.ModelSerializer):
    student = UserSerializer()

    class Meta:
        model = PendingApproval
        fields = ('id', 'student')
