from datetime import datetime
import re
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils.deconstruct import deconstructible
import os
import socket
from PIL import Image

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

path_and_rename_user_avatar = PathAndRename("profile/")

# get ip address via the function
def get_ip():
    hostname=socket.gethostname()
    ip=socket.gethostbyname(hostname)
    return ip

class User(AbstractUser):
    password = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(upload_to=path_and_rename_user_avatar, blank=True)
    about_me = models.CharField(max_length=2048, blank=True)
    website_url = models.URLField(max_length=256, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            return            

        try:
            old_avatar = User.objects.get(pk=self.pk).avatar
            print("old", old_avatar.path)
            os.remove(old_avatar.path)
        except:
            print("error")
        quality_value = 100
        super(User, self).save(*args, **kwargs)
        image = Image.open(self.avatar)
        (width, height) = image.size     
        size = ( 200, 200)
        image = image.resize(size, Image.LINEAR)
        image.save(self.avatar.path, quality=quality_value)

class UserFollower(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')
    to = models.ForeignKey(User,on_delete=models.CASCADE, related_name='following')
    date = models.DateTimeField(default=datetime.now)
    ip = models.CharField(max_length=256,default=get_ip())
    is_accepted = models.BooleanField(default=False)
