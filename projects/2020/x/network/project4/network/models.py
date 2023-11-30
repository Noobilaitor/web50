from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.CharField(max_length=300)