from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from slugify import slugify
from tag.models import Tag
from .models import  Post, PostAction
from .forms import PostForm
from django.utils.decorators import method_decorator
import re
import hashlib
import time
from uuid import uuid4

# functions 
# get tags from post descriptions
def getTagsFromText(text):
    arrayWithHastag = re.findall(r'(?:^|\s)(#\w+)', text)
    return [s.strip('#') for s in arrayWithHastag]

# generate random string for permalink
def generateRandomPermalink(stringForSalting):
    saltText = str(time.time()) + uuid4().hex + stringForSalting 
    return hashlib.sha512(saltText.encode()).hexdigest()[:16]

# Create your views here.
class DetailView(View):
    template_name = 'post/detail.html'
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post,hashed_permalink=self.kwargs['permalink'])
        return render(request, self.template_name, {'post': post})

class CreateView(View):
    form_class = PostForm
    template_name = 'post/create.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    @method_decorator(login_required)
    def post(self, request):
        current_user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # remove tags from description after adding to the database
            description_without_tags = form['description'].value()
            hashed_permalink = generateRandomPermalink(request.user.username)
            print("hashedPermalink",hashed_permalink)
            # create process
            post = Post.objects.create(description=form['description'].value(),image=form['image'].value(), posted_user=current_user, hashed_permalink=hashed_permalink)
            # create tags by post description
            tagNames = getTagsFromText(form.cleaned_data['description'])
            for tagName in tagNames:
                description_without_tags = description_without_tags.replace("#" + tagName, "")
                try:
                    tag_entity = Tag.objects.get(name=tagName)
                    post.tags.add(tag_entity)
                except Tag.DoesNotExist:
                    # save tags to the database
                    tag_new = Tag.objects.create(name=tagName)
                    tag_new.save()
                    post.tags.add(tag_new)
            # post.description = description_without_tags
            post.description = description_without_tags
            post.save()
            return HttpResponseRedirect(reverse("post:detail", args=(post.hashed_permalink,)))

        return render(request, self.template_name, {'form': form})


class ActionView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        action_id = 0
        if self.kwargs['action_name'] == "save": action_id=1
        # get authenticated user
        current_user = request.user
        # get post by permalink 
        post = get_object_or_404(Post,hashed_permalink=self.kwargs['permalink'])
        try:
            old_like__action = PostAction.objects.get(post=post, user=current_user, action_number=action_id)
            # remove the action
            old_like__action.delete()
            return HttpResponse("canceled")     
        except PostAction.DoesNotExist:
            # create new like action
            post_like__action = PostAction(user=current_user, post=post, action_number=action_id) # zero (0) value is for like action
            post_like__action.save()
            return HttpResponse("acted")
            