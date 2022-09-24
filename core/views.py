from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def home(request):
    section_title = "My"
    return render(request, "core/index.html", {
        "title": section_title
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