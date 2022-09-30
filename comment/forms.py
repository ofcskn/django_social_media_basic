from django.forms import ModelForm
from django import forms
from account.models import User
from post.models import PostComment

class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']