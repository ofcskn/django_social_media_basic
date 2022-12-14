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
from django.http import JsonResponse
from uuid import uuid4
import socket
import json

# functions 
# get ip address via the function
def get_ip():
    hostname=socket.gethostname()
    ip=socket.gethostbyname(hostname)
    return ip

class GetAllByPostView(View):
    template_name = 'comment/partials/_comment_for_post.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # get post by permalink 
        post = get_object_or_404(Post,hashed_permalink=self.kwargs['permalink'])
        post_comments = PostComment.objects.all().filter(for_post=post).values()
        return JsonResponse({"post_comments": list(post_comments)}, safe=False)

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


class EditView(View):
    form_class = PostCommentForm
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # get comment by id
            comment = get_object_or_404(PostComment, id=self.kwargs['id'])
            if comment.who_sent == request.user:
                comment.content = form.cleaned_data['content']
                comment.save()
                return HttpResponse("success")
            else:
                return HttpResponse(401)               

class ReplyView(View):
    form_class = PostCommentForm
    template_name = 'comment/partials/_comment_for_post.html'
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # get comments by id
            to_comment = get_object_or_404(PostComment, id=self.kwargs['id'])
            comment = PostComment(content=form.cleaned_data['content'], who_sent=request.user, ip=get_ip(), sub_comment=to_comment, for_post=to_comment.for_post)
            comment.save()
            return render(request, self.template_name, {"comment": comment})
        else:
            return HttpResponse("not-valid")            

class DeleteView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # get comment by id
        comment = get_object_or_404(PostComment, id=self.kwargs['id'])
        if comment.who_sent == request.user:
            comment.delete()
            return HttpResponse("success")
        else:
            return HttpResponse(401)            