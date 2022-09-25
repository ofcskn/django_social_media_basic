from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils.deconstruct import deconstructible
import os

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

class User(AbstractUser):
    password = models.CharField(max_length=64, blank=True)
    avatar = models.FileField(upload_to=path_and_rename_user_avatar, default="default.png")

