from urllib import request
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.conf import settings
from post.models import Post, PostAction # import the settings file
from django.views import View
from account.models import User, UserFollower
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import F, Sum, Q

from tag.models import Tag

# Create your views here.
class HomeView(View):
    template_name = 'core/index.html'
    @method_decorator(login_required)
    def get(self, request):
        take_count = 10
        # order by descending posts and take take_count posts for initializing
        posts = Post.objects.filter(~Q(posted_user=request.user)).order_by("-created_date")[:take_count]
        tags = Tag.objects.all()[:20]
        newUsers = User.objects.all().filter().order_by("-date_joined")[:20]
        return render(request, self.template_name, {"posts": posts, "tags": tags, "newUsers": newUsers})

class ExploreView(View):
    template_name = 'core/explore.html'
    # order by descending posts and take take_count posts for initializing
    take_count = 5
    posts = Post.objects.all().order_by("?")[:take_count]
    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {"posts": self.posts})

# search
class SearchView(View):
    template_name = 'core/search.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        qSearch = request.GET.get('q', "")
        tags = Tag.objects.filter(Q(name__contains=qSearch))[:6]
        users = User.objects.filter(Q(username__contains=qSearch) | Q(first_name__contains=qSearch) | Q(last_name__contains=qSearch)).order_by("-date_joined")[:6]
        posts = Post.objects.filter(description__contains=qSearch).order_by("-created_date")[:6]
        return render(request, self.template_name, {"posts": posts, "tags":tags, "users":users})

# profile view
class ProfileView(View):
    template_name = 'core/profile.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # constants
        postTakeCount = 9
        user = get_object_or_404(User, username=self.kwargs['user_name'])
        # check the user is following by authenticated user
        userIsFollowing = UserFollower.objects.filter(to=user,follower=request.user).count() > 0
        # get followers of the user
        followers_of = UserFollower.objects.filter(to=user, is_accepted=True).count()
        following_of = UserFollower.objects.filter(follower=user, is_accepted=True).count()
        postsAll = Post.objects.order_by("-created_date").filter(posted_user=user)
        postsCount = postsAll.count()
        return render(request, self.template_name, {"profile_user": user, "posts": postsAll[:postTakeCount], "postsCount": postsCount, 'userIsFollowing': userIsFollowing,'following_of':following_of, 'followers_of':followers_of })

@login_required()
def follow_user(request, to_user_name):
    if request.method == "POST":
        currentUser = request.user 
        toUser = get_object_or_404(User,username=to_user_name)
        try:
            old_following__request = UserFollower.objects.get(to=toUser, follower=currentUser)
            # remove user request
            old_following__request.delete()
            return HttpResponse("canceled")     
        except UserFollower.DoesNotExist:
            # create user follower data
            userFollower = UserFollower(to=toUser,follower=currentUser)
            userFollower.save()
            return HttpResponse("sent")
    else:
        return HttpResponse("failed-request")

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