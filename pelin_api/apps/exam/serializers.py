from rest_framework import serializers
from .models import Exam, Question


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        extra_kwargs = {
            'group': {'required': False, 'write_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        extra_kwargs = {
            'exam': {'required': False, 'write_only': True}
        }
