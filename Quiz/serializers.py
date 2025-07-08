# Quiz/serializers.py
from rest_framework import serializers
from .models import (
    Teacher, Student, QuestionPaper, QuestionBank, TestResult
)

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Teacher
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = "__all__"

class QuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model  = QuestionPaper
        fields = "__all__"

class QuestionBankSerializer(serializers.ModelSerializer):
    class Meta:
        model  = QuestionBank
        fields = "__all__"

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TestResult
        fields = "__all__"
