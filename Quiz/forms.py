from django import forms
from django.forms import ModelForm
from .models import *
from .models import Teacher, Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']


class TeacherSignupForm(forms.ModelForm):
    class Meta:
        model  = Teacher
        fields = ("name", "email", "teacher_id", "password")
        widgets = {"password": forms.PasswordInput()}


class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ("student_id", "name")