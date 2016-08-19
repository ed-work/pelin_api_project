from rest_framework import serializers
from .models import Exam, Question, Score
from apps.core.serializers import UserSerializer


class ExamSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        return obj.get_score(self.context.get('request').user)

    def __init__(self, *args, **kwargs):
        super(ExamSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request'):
            if self.context.get('request').user.is_teacher():
                self.fields.pop('score')

    class Meta:
        model = Exam
        extra_kwargs = {
            'group': {'required': False, 'write_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request'):
            if not self.context.get('request').user.is_teacher():
                self.fields.pop('answer_key')

    class Meta:
        model = Question
        extra_kwargs = {
            'exam': {'required': False, 'write_only': True}
        }


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        print self.context.get('request')
        ss = UserSerializer(
            obj.user,
            fields=('id', 'name', 'student', 'photo'),
            context={'request': self.context.get('request')})
        return ss.data

    class Meta:
        model = Score
