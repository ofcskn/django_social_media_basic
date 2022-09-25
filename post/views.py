from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import  Post
from .forms import PostForm

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
    def get(self, request, *args, **kwargs):
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
