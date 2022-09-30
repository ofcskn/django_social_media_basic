from django.forms import ModelForm
from django import forms
from account.models import User
from .models import Post, PostComment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']

class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']