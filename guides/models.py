from datetime import datetime
from os.path import splitext

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver


def _upload_path(instance, filename):
    return instance.get_upload_path(filename)


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=_upload_path,
                               null=True,
                               blank=True,
                               verbose_name='Аватар')

    def get_upload_path(self, filename):
        return str(self.username) + "/avatar/" \
               + splitext(filename)[0] + '.' + str(datetime.now().timestamp()) + splitext(filename)[1]

    REQUIRED_FIELDS = ['first_name', 'last_name']


class Guide(models.Model):
    """Модель Руководства"""

    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    cover = models.ImageField(upload_to=_upload_path,
                              null=True,
                              blank=True,
                              verbose_name='Обложка')
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                               verbose_name='Автор')

    def get_upload_path(self, filename):
        return str(self.author.username) + "/guides/" + str(self.name) + '__' \
               + splitext(filename)[0] + '__' + str(datetime.now().timestamp()) + splitext(filename)[1]

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Гайд'
        verbose_name_plural = 'Гайды'


@receiver(pre_delete, sender=Guide)
def cover_delete(sender, instance, **kwargs):
    if instance.cover.name:
        instance.cover.delete(False)


@receiver(pre_delete, sender=CustomUser)
def avatar_delete(sender, instance, **kwargs):
    if instance.avatar.name:
        instance.avatar.delete(False)
