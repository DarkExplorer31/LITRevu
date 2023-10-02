from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_photo = models.ImageField()
    quote = models.CharField(max_length=255, null=True)