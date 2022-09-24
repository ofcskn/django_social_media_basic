from datetime import datetime
from django.db import models
from account.models import User

class Post(models.Model):
    description = models.CharField(max_length=2056)
    posted_user_id = models.ForeignKey("account.User", on_delete=models.CASCADE)
    image = models.FileField(upload_to='posts/%Y/%m/%D/', blank=True)
    created_date = models.DateTimeField(default= datetime.now)