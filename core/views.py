from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.conf import settings
from .forms import PostForm
from core.models import Post # import the settings file
from django.views import View
from account.models import User
from django.contrib.auth.decorators import login_required

@login_required
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

@login_required
def explore(request):
    return HttpResponse("this is explore page")

@login_required
def get_user(request, user_name):
    return HttpResponse(user_name)
    
@login_required
def get_followers_of_user(request, user_name):
    return HttpResponse("Followers of " + user_name)

@login_required
def saved_posts_of_user(request, user_name):
    return HttpResponse("Saved posts of " + user_name)

@login_required
def liked_posts_of_user(request, user_name):
    return HttpResponse("Liked posts of " + user_name)

class CreatePostView(View):
    form_class = PostForm
    template_name = 'core/create_post.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        current_user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # create process
            post = Post.objects.create(description=form['description'].value(),image=form['image'].value(), posted_user=current_user)
            post.save()
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {'form': form})
