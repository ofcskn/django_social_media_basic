from django.db import models

# Create your models here.

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=64)
    email = models.EmailField()
    phone_number = models.CharField(max_length=16,blank=True)
    password_hash = models.CharField(max_length=64, blank=True)
    avatar = models.FileField(upload_to='profile/%Y/%m/%D/', blank=True)
    status = models.BooleanField(default=False)
