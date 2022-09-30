from django.contrib import admin
from .models import Post, PostAction, PostComment

# Register your models here.
admin.site.register(Post)
admin.site.register(PostAction)
