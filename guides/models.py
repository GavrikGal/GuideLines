from datetime import datetime
from os.path import splitext

from django.db import models
from django.contrib.auth.models import AbstractUser


def _upload_path(instance, filename):
    return instance.get_upload_path(filename)


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=_upload_path,
                               null=True,
                               blank=True)

    def get_upload_path(self, filename):
        return "avatar/" + str(self.username) + "/" \
               + splitext(filename)[0] + '.' + str(datetime.now().timestamp()) + splitext(filename)[1]

    REQUIRED_FIELDS = ['first_name', 'last_name']

    # + str(datetime.now().timestamp())


