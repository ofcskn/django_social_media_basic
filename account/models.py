from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    password = models.CharField(max_length=64, blank=True)
    avatar = models.FileField(upload_to='profile/%Y/%m/%D/', blank=True)

