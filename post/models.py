from datetime import datetime
from django.db import models
import os
from uuid import uuid4
from django.conf import settings
from django.utils.deconstruct import deconstructible
import socket

from account.models import User
from tag.models import Tag


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

# get ip address via the function
def get_ip():
    hostname=socket.gethostname()
    ip=socket.gethostbyname(hostname)
    return ip

path_and_rename = PathAndRename("posts/")

class Post(models.Model):
    description = models.CharField(max_length=2056)
    posted_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.FileField(upload_to=path_and_rename, blank=True)
    created_date = models.DateTimeField(default= datetime.now)
    tags = models.ManyToManyField(Tag)
    
    @property
    def total_like_count(self):
        return PostAction.objects.filter(post=self, action_number=0).count()

    @property
    def total_save_count(self):
        return PostAction.objects.filter(post=self, action_number=1).count()

class PostAction(models.Model):
    action_number = models.IntegerField(default=0) # default (0) is for like action. (1) is for saving post
    date = models.DateTimeField(default=datetime.now)
    ip = models.CharField(max_length=256,default=get_ip())
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="acted_user")
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_for")