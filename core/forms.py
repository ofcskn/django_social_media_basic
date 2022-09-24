from django.forms import ModelForm
from django import forms
from core.models import Post, User

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['name', 'email', 'username']