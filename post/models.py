from datetime import datetime
from email.policy import default
from enum import unique
from pickletools import optimize
from PIL import Image
from django.db import models
import os, sys
from uuid import uuid4
from django.conf import settings
from django.utils.deconstruct import deconstructible
import socket

from account.models import User
from tag.models import Tag
from slugify import slugify


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

class Post(models.Model):
    description = models.CharField(max_length=2056)
    posted_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.FileField(upload_to=PathAndRename("posts/"), blank=True)
    created_date = models.DateTimeField(default= datetime.now)
    tags = models.ManyToManyField(Tag)
    hashed_permalink = models.CharField(max_length=16,unique=True)

    def save(self, *args, **kwargs):
        if not self.image:
            return            

        upload_sizes = [(1500,1500), (500,500), (250,250),(0,0)] # 0x0 is for original size
        super(Post, self).save(*args, **kwargs)

        normalPathWithoutExtension = os.path.splitext(self.image.path)[0]
        extension = os.path.splitext(self.image.path)[1]
        for size in upload_sizes:   
            image = Image.open(self.image)
            if size != (0, 0):
                # upload alternative images
                upload_path = normalPathWithoutExtension + "x" + str(size[0]) + "x" + str(size[1]) + extension
                image = image.resize(size, Image.ANTIALIAS)
                image.save(upload_path) 
            else:
                # upload original image
                upload_path =   normalPathWithoutExtension + extension
                image.save(upload_path)
        
    @property
    def total_like_count(self):
        return PostAction.objects.filter(post=self, action_number=0).count()

    @property
    def total_save_count(self):
        return PostAction.objects.filter(post=self, action_number=1).count()
    
    @property
    def total_comment_count(self):
        return PostComment.objects.filter(for_post=self).count()


class PostAction(models.Model):
    action_number = models.IntegerField(default=0) # default (0) is for like action. (1) is for saving post
    date = models.DateTimeField(default=datetime.now)
    ip = models.CharField(max_length=256,default=get_ip())
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="acted_user")
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_for")

class PostComment(models.Model):
    who_sent=models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_sent")
    content= models.CharField(max_length=512)
    date = models.DateTimeField(default=datetime.now)
    ip= models.GenericIPAddressField()
    for_post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    sub_comment=models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)     