from django.forms import ModelForm
from django import forms
from .models import  User

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'about_me', 'website_url']

class ProfileAvatarUploadForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

class ProfileChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)
    password_repeat = forms.CharField(max_length=32)