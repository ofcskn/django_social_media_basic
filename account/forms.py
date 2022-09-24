from django.forms import ModelForm
from django import forms
from .models import  User

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['name', 'email', 'username']