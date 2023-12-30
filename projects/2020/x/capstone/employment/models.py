from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='', default='default.png')
    employee = models.BooleanField(default=False)
    employer = models.BooleanField(default=False)
    has_CV = models.BooleanField(default=False)
    has_job = models.BooleanField(default=False)
    CV_requests = models.ManyToManyField("self",)
    job_requests = models.ManyToManyField("self",)
    working = models.ManyToManyField("self", null=True, blank=True)

class CV(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE, related_name="my_CV")
    skills = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    education = models.CharField(max_length=1000)
    career = models.CharField(max_length=1000)
    job = models.CharField(max_length=64, default="engineer")
    major = models.CharField(max_length=64, default="chemical engineering")
    is_active = models.BooleanField(default=True)

class Job(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    salary = models.CharField(max_length=64, default="0")
    job = models.CharField(max_length=64, default="engineer")
    major = models.CharField(max_length=64, default="chemical engineering")
    is_active = models.BooleanField(default=True)   
