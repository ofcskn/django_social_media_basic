from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from slugify import slugify
from tag.models import Tag
from post.models import  Post, PostAction, PostComment
from .forms import PostCommentForm
from django.utils.decorators import method_decorator
import re
import hashlib
import time
from uuid import uuid4
import socket

# functions 
# get ip address via the function
def get_ip():
    hostname=socket.gethostname()
    ip=socket.gethostbyname(hostname)
    return ip

class SendView(View):
    form_class = PostCommentForm
    template_name = 'comment/partials/_comment_for_post.html'
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # get authenticated user
        current_user = request.user
        # get post by permalink 
        post = get_object_or_404(Post,hashed_permalink=self.kwargs['permalink'])
        # filling the form
        form = self.form_class(request.POST)
        if form.is_valid():
            post_comment = PostComment(who_sent= current_user,for_post=post, ip= get_ip(), content=form.cleaned_data['content'])
            post_comment.save()
            return render(request, self.template_name, {"comment": post_comment})
        else:
            return HttpResponse("not-valid")
        
            