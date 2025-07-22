from django import forms
from .models import *
from .models import Teacher, Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']

class ExtendedUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, label="Full Name")
    teacher_id = forms.CharField(max_length=30, label="Teacher ID")

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "name", "teacher_id"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Teacher.objects.filter(email=username).exists():
            raise forms.ValidationError("A teacher with this email already exists.")
        return username

class TeacherSignupForm(forms.ModelForm):
    class Meta:
        model  = Teacher
        fields = ("name", "email", "teacher_id", "password")
        widgets = {"password": forms.PasswordInput()}


class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ("student_id", "name")