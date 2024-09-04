from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.base.models import BaseModel
from apps.user.managers import UserManager


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    number = models.CharField(unique=True, max_length=11, null=True)
    username = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()
