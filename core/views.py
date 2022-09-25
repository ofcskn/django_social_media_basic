from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.conf import settings
from post.models import Post # import the settings file
from django.views import View
from account.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class HomeView(View):
    template_name = 'core/index.html'
    # order by descending posts and take take_count posts for initializing
    take_count = 10
    posts = Post.objects.order_by("-created_date")[:take_count]
    def get(self, request):
        return render(request, self.template_name, {"posts": self.posts})

# profile view
class ProfileView(View):
    template_name = 'core/profile.html'
    def get(self, request, *args, **kwargs):
        # constants
        postTakeCount = 9

        user = get_object_or_404(User, username=self.kwargs['user_name'])

        postsAll = Post.objects.order_by("-created_date").filter(posted_user=user)
        postsCount = postsAll.count()
        return render(request, self.template_name, {"user": user, "posts": postsAll[:postTakeCount], "postsCount": postsCount})


@login_required
def explore(request):
    return HttpResponse("this is explore page")
    
@login_required
def get_followers_of_user(request, user_name):
    return HttpResponse("Followers of " + user_name)

@login_required
def saved_posts_of_user(request, user_name):
    return HttpResponse("Saved posts of " + user_name)

@login_required
def liked_posts_of_user(request, user_name):
    return HttpResponse("Liked posts of " + user_name)