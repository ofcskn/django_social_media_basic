from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.conf import settings

from core.models import Post # import the settings file

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

def create_post(request, post):
    return HttpResponse("Creating post page")