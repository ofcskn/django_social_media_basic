from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import  Post, PostAction
from .forms import PostForm
from django.utils.decorators import method_decorator

# Create your views here.
class DetailView(View):
    template_name = 'post/detail.html'
    def get(self, request, *args, **kwargs):
        print('get_called')
        post = get_object_or_404(Post,pk=self.kwargs['id'])
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
            # create process
            post = Post.objects.create(description=form['description'].value(),image=form['image'].value(), posted_user=current_user)
            post.save()
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {'form': form})


class ActionView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        action_id = 0
        if self.kwargs['action_name'] == "save": action_id=1
        # get authenticated user
        current_user = request.user
        # get post by id 
        post = get_object_or_404(Post,pk=self.kwargs['id'])
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
            