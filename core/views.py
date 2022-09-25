from mimetypes import init
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.conf import settings
from .forms import PostForm
from core.models import Post # import the settings file
from django.core.files.storage import FileSystemStorage
import hashlib, uuid, random
from django.views import View
from account.models import User
from django.forms import inlineformset_factory

# Create your views here.
def home(request):
    section_title = "My"
    # post list of the user (firstly)
    posts = Post.objects.all()
    return render(request, "core/index.html", {
        "title": section_title,
        "user_name": "ofcskn",
        "posts": posts,
        "app_name": settings.APP_NAME
    })

def explore(request):
    return HttpResponse("this is explore page")

def get_user(request, user_name):
    return HttpResponse(user_name)
    
def get_followers_of_user(request, user_name):
    return HttpResponse("Followers of " + user_name)
        
def saved_posts_of_user(request, user_name):
    return HttpResponse("Saved posts of " + user_name)

def liked_posts_of_user(request, user_name):
    return HttpResponse("Liked posts of " + user_name)


class CreatePostView(View):
    form_class = PostForm
    template_name = 'core/create_post.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        userId = 1 # constant for now
        user = User.objects.get(pk=userId)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # create process
            post = Post.objects.create(description=form['description'].value(),image=form['image'].value(), posted_user_id=user)
            post.save()
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {'form': form})
