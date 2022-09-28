from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
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
        # get following of the authenticated user for related posts
        userFollowings = UserFollower.objects.filter(follower=request.user, is_accepted=True).values_list("to")
        # order by descending posts and take take_count posts for initializing
        posts = Post.objects.filter(~Q(posted_user=request.user)).filter(posted_user__in=userFollowings).order_by("-created_date")[:take_count]
        if posts.count() == 0:
            posts = Post.objects.filter(~Q(posted_user=request.user)).order_by("-created_date")[:take_count]
        tags = Tag.objects.all()[:20]
        newUsers = User.objects.all().filter().order_by("-date_joined")[:20]
        return render(request, self.template_name, {"posts": posts, "tags": tags, "newUsers": newUsers})

class ExploreView(View):
    template_name = 'core/explore.html'
    # order by descending posts and take take_count posts for initializing
    take_count = 9
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
        posts = Post.objects.filter(Q(description__contains=qSearch) | Q(tags__name__exact=qSearch)).order_by("-created_date")[:6]
        return render(request, self.template_name, {"posts": posts, "tags":tags, "users":users})

# profile view
class ProfileView(View):
    template_name = 'core/profile.html'
    @method_decorator(login_required)
    def get(self, request, type="", *args, **kwargs):
        # constants
        postTakeCount = 9
        user = get_object_or_404(User, username=self.kwargs['user_name'])
        # check the user is following by authenticated user
        userFollowingType = "not-following"
        userFollowers = UserFollower.objects.filter(to=user,follower=request.user)
        if userFollowers.filter(is_accepted=True).count() > 0:
            userFollowingType = "accepted"
        elif userFollowers.filter(is_accepted=False).count() > 0:
            userFollowingType = "pending"    

        # get followers of the user
        followers_of = UserFollower.objects.filter(to=user, is_accepted=True).count()
        following_of = UserFollower.objects.filter(follower=user, is_accepted=True).count()
        context = {"profile_user": user,'userFollowingType': userFollowingType,'following_of':following_of, 'followers_of':followers_of, "postActions": {} }
        if type == "saved":
            postsAllSaved = PostAction.objects.order_by("-date").filter(action_number=1,user=request.user)[:postTakeCount]
            print(postsAllSaved)
            context['postActions']['saved'] = postsAllSaved
        elif type == "liked":
            postsAllLiked = PostAction.objects.order_by("-date").filter(action_number=0,user=request.user)[:postTakeCount]
            context['postActions']['liked'] = postsAllLiked
        else:
            postsAll = Post.objects.order_by("-created_date").filter(posted_user=user)[:postTakeCount]
            context['posts'] = postsAll
        return render(request, self.template_name, context)

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
def get_followers_of_user(request, user_name):
    return HttpResponse("Followers of " + user_name)
