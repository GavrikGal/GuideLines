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
        return str(self.username) + "/avatar/" \
               + splitext(filename)[0] + '.' + str(datetime.now().timestamp()) + splitext(filename)[1]

    REQUIRED_FIELDS = ['first_name', 'last_name']


class Guide(models.Model):
    """Модель Руководства"""

    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='media',
                              null=True,
                              blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def get_upload_path(self, filename):
        return str(self.author.username) + "/guides/" + str(self.name) + '/' \
               + splitext(filename)[0] + '.' + str(datetime.now().timestamp()) + splitext(filename)[1]

    REQUIRED_FIELDS = ['name']
