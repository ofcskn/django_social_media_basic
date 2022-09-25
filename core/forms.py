from django.forms import ModelForm
from django import forms
from account.models import User
from core.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']

