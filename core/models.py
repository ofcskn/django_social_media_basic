from datetime import datetime
from django.db import models
import os
from uuid import uuid4
from django.conf import settings
from django.utils.deconstruct import deconstructible

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

path_and_rename = PathAndRename("/posts")

class Post(models.Model):
    description = models.CharField(max_length=2056)
    posted_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.FileField(upload_to=path_and_rename, blank=True)
    created_date = models.DateTimeField(default= datetime.now)