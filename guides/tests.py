import os
from abc import ABC, abstractmethod
from os.path import splitext
from shutil import rmtree

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import CustomUser, Guide


TEST_USERNAME = 'username_gal_test'
TEST_PASSWORD = 'Password12345'
TEST_FIRST_NAME = 'Дмитрий'
TEST_LAST_NAME = 'Гал'
TEST_AVATAR_IMG_NAME = 'gal-avatar-12345.jpg'

TEST_GUIDE_NAME = 'Моё первое тестовое руководство'
TEST_GUIDE_DESCRIPTION = 'Моё описание к первому тестовому руководству. Должно быть много букф, но ' \
                         'надо немного сократиться. Пока. Это было круто'
TEST_GUIDE_COVER_IMG_NAME = 'gal-guide-cover-12345.jpg'


class BaseUnitTest(TestCase):
    """Базовый класс для юнит-тестов"""

    @classmethod
    def tearDownClass(cls) -> None:
        # Удаление мусора (всей папки TEST_USERNAME) после завершения теста
        if os.listdir(settings.MEDIA_ROOT / TEST_USERNAME):
            rmtree(settings.MEDIA_ROOT / TEST_USERNAME, ignore_errors=True)


class UnitTest(TestCase):
    """Модульное тестирование"""

    def test_can_start_test(self) -> None:
        """тесты могут запускаться"""
        self.assertEqual(1 + 2, 3)


class CustomUserModelTest(BaseUnitTest):
    """Модульное тестирование модели пользователя"""

    def test_custom_user_avatar_upload_path(self) -> None:
        """тест пути загрузки аватарки пользователя"""
        user = CustomUser.objects.create(username=TEST_USERNAME,
                                         first_name=TEST_FIRST_NAME,
                                         last_name=TEST_LAST_NAME)

        user.avatar = SimpleUploadedFile(TEST_AVATAR_IMG_NAME, b'', content_type='image/jpeg')
        user.save()

        self.assertIn(
            user.username + '/avatar/' + splitext(TEST_AVATAR_IMG_NAME)[0],
            user.avatar.name
        )


class GuideModelTest(BaseUnitTest):
    """Модульное тестирование модели руководства"""

    def test_guide_cover_upload_path(self) -> None:
        """тест пути загрузки обложки Руководства"""
        user = CustomUser.objects.create(username=TEST_USERNAME,
                                         first_name=TEST_FIRST_NAME,
                                         last_name=TEST_LAST_NAME,
                                         avatar=TEST_AVATAR_IMG_NAME)

        guide = Guide.objects.create(name=TEST_GUIDE_NAME,
                                     description=TEST_GUIDE_DESCRIPTION,
                                     author=user)

        guide.cover = SimpleUploadedFile(TEST_GUIDE_COVER_IMG_NAME, b'', content_type='image/jpeg')
        guide.save()

        self.assertIn(
            user.username + '/guides/' + guide.name + '/' + splitext(TEST_GUIDE_COVER_IMG_NAME)[0],
            guide.cover.name
        )
