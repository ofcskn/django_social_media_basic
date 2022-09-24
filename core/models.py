from datetime import datetime
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=64)
    email = models.EmailField()
    phone_number = models.CharField(max_length=16,blank=True)
    password_hash = models.CharField(max_length=64)
    image_name = models.CharField(max_length=256)
    status = models.BooleanField(default=False)


class Post(models.Model):
    description = models.CharField(max_length=2056)
    posted_user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    image_name = models.CharField(max_length=256)
    created_date = models.DateTimeField(default= datetime.now)
    