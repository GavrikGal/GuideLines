from os.path import exists
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


class ReadyUnitTest(TestCase):
    """Модульное тестирование"""

    def test_can_start_test(self) -> None:
        """тесты могут запускаться"""
        self.assertEqual(1 + 2, 3)


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
