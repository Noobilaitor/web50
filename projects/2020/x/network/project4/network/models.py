from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    likes_num = models.IntegerField(default=0)
    

class Followers(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    class Meta:
       unique_together = ('following', 'followers',)
       