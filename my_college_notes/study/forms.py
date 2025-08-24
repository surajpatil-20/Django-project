from django import forms
from .models import UploadedFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file', 'year', 'department']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
