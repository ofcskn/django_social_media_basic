from datetime import datetime
from django.db import models
import os
from uuid import uuid4

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

class Post(models.Model):
    description = models.CharField(max_length=2056)
    posted_user_id = models.ForeignKey("account.User", on_delete=models.CASCADE)
    image = models.FileField(upload_to=path_and_rename('posts/'), blank=True)
    created_date = models.DateTimeField(default= datetime.now)