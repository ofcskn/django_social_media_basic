from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.conf import settings
from .forms import PostForm, UserForm
from core.models import Post # import the settings file
from django.core.files.storage import FileSystemStorage
import hashlib, uuid, random

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

# view for post creating
def create(request):
    return render(request, "core/create_post.html", {
        "title": "Create a Post",
        "user_name": "ofcskn",
        "app_name": settings.APP_NAME
    })

# post for adding a post
def create_post(request):
    if request.method == 'POST':
        # add the post to the database
        form = PostForm(request.POST, request.FILES)
        print('form', form.is_valid())
        if form.is_valid():
            salt = uuid.uuid4().hex
            #hashed_file_name = hashlib.sha512(post_file.name + salt).hexdigest()
            #fs = FileSystemStorage()
            #filename = fs.save(hashed_file_name, post_file)
            #uploaded_file_url = fs.url(filename)
            #print(uploaded_file_url)
            form.save()
            return HttpResponseRedirect('success')
        pass
    else:
        form = PostForm()
    return HttpResponse('not-valid')
    # return render(request, "core/create_post.html", {
    #     "title": "Create a Post",
    #     "user_name": "ofcskn",
    #     "app_name": settings.APP_NAME
    # })

# create user
def create_user(request):
    if request.method == 'POST':
        # add the user to the database
        user = UserForm(request.POST, request.FILES)
        print('form', form.is_valid())
        if user.is_valid():
            salt = uuid.uuid4().hex + "salt_try"
            hashed_password = hashlib.sha512(user.password + salt).hexdigest()
            user.password_hashed = hashed_password
            print('user: ', user)
            user.save()
            return HttpResponseRedirect('success')
        pass
    else:
        form = PostForm()
    return HttpResponse('not-valid')
    # return render(request, "core/create_post.html", {
    #     "title": "Create a Post",
    #     "user_name": "ofcskn",
    #     "app_name": settings.APP_NAME
    # })

