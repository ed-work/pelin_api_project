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
    class Meta:
        model = Question
        extra_kwargs = {
            'exam': {'required': False, 'write_only': True},
            'answer_key': {'write_only': True}
        }


class ScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer(fields=['id', 'name', 'student'])

    class Meta:
        model = Score
