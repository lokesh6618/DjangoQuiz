from rest_framework import viewsets, permissions, mixins
from .models import Teacher, Student, QuestionPaper, QuestionBank, TestResult
from .serializers import (
    TeacherSerializer, StudentSerializer,
    QuestionPaperSerializer, QuestionBankSerializer, TestResultSerializer,
)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset         = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset         = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = ["teacher"]      # optional filter ?teacher=<id>

class QuestionPaperViewSet(viewsets.ModelViewSet):
    queryset         = QuestionPaper.objects.all()
    serializer_class = QuestionPaperSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionBankViewSet(viewsets.ModelViewSet):
    queryset         = QuestionBank.objects.all()
    serializer_class = QuestionBankSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["paper"]

class TestResultViewSet(viewsets.ModelViewSet):
    queryset         = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["student", "paper"]
