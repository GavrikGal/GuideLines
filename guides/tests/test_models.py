from os.path import exists
from os.path import splitext
from shutil import rmtree
from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import signals

from ..models import CustomUser, Guide

import guides.models

from .utils.const import (
    TEST_USERNAME, TEST_AVATAR_IMG_NAME, TEST_GUIDE_COVER_IMG_NAME
)


class CustomUserModelTest(TestCase):
    """Модульное тестирование модели пользователя"""

    def test_custom_user_avatar_upload_path(self) -> None:
        """тест пути загрузки аватарки пользователя"""

        user = CustomUser(username=TEST_USERNAME)
        upload_path = user.get_upload_path(TEST_AVATAR_IMG_NAME)

        self.assertIn(
            user.username + '/' + splitext(TEST_AVATAR_IMG_NAME)[0],
            upload_path
        )

    def test_media_is_upload(self) -> None:
        """тест загружаются ли медиаданные указанные в ImageField модели
        в место хранинения media"""

        user = CustomUser(username=TEST_USERNAME)
        user.avatar = SimpleUploadedFile(TEST_AVATAR_IMG_NAME, b'', content_type='image/jpeg')
        user.save()

        upload_path = user.avatar.name
        absolut_upload_path = settings.MEDIA_ROOT / upload_path

        self.assertTrue(
            exists(absolut_upload_path)
        )

        if exists(settings.MEDIA_ROOT / TEST_USERNAME):
            rmtree(settings.MEDIA_ROOT / TEST_USERNAME, ignore_errors=True)

    def test_delete_user_root_dir_calling(self) -> None:
        """тест: функция удаления корневой медиа-директрории пользователя
        delete_user_root_dir зарегистирована в с сигланах pre_delete моделей джанго"""

        registered_functions = [r[1]() for r in signals.pre_delete.receivers]
        self.assertIn(
            guides.models.delete_user_root_dir,
            registered_functions
        )


class GuideModelTest(TestCase):
    """Модульное тестирование модели Руководства"""

    def test_guide_cover_upload_path(self) -> None:
        """тест пути загрузки обложки Руководства"""

        user = CustomUser(username=TEST_USERNAME)
        guide = Guide(author=user)
        upload_path = guide.get_upload_path(TEST_GUIDE_COVER_IMG_NAME)

        self.assertIn(
            user.username + '/' + splitext(TEST_GUIDE_COVER_IMG_NAME)[0],
            upload_path
        )
