from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='', default='default.png')
    employee = models.BooleanField(default=False)
    employer = models.BooleanField(default=False)
    has_CV = models.BooleanField(default=False)

class CV(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE, related_name="my_CV")
    skills = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    education = models.CharField(max_length=1000)
    career = models.CharField(max_length=1000)
