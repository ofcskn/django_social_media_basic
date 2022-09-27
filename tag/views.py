from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import  Tag
from post.models import  Post
from django.utils.decorators import method_decorator

# Create your views here.
class DetailView(View):
    template_name = 'tag/detail.html'
    def get(self, request, *args, **kwargs):
        tag = get_object_or_404(Tag,permalink=self.kwargs['tag_permalink'])
        # get posts by the tag
        posts_by_tag = Post.objects.filter(tags__pk=tag.pk)
        return render(request, self.template_name, {'posts': {
            "all": posts_by_tag,
            "count": posts_by_tag.count() 
        }, 'tag': tag})
