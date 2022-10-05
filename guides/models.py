from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='',
                               null=True,
                               blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']

