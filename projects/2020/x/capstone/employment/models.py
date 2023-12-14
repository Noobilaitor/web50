from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='', default='employment/media/employmentdefault.png')
    employee = models.BooleanField(default=False)
    employer = models.BooleanField(default=False)
