from os.path import splitext
from shutil import rmtree

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import CustomUser


TEST_USERNAME = 'gal_test'
TEST_PASSWORD = 'Password12345'
TEST_FIRST_NAME = 'Дмитрий'
TEST_LAST_NAME = 'Гал'
TEST_AVATAR_IMG_NAME = 'gal-avatar-12345.jpg'

TEST_MEDIA_CONTENT = '/functional_tests/img/Avatar.jpg'


class UnitTest(TestCase):
    """Модульное тестирование"""

    def test_can_start_test(self) -> None:
        """тесты могут запускаться"""
        self.assertEqual(1 + 2, 3)


class CustomUserModelTest(TestCase):
    """Модульное тестирование модули пользователя"""
    def test_custom_user_avatar_upload_path(self) -> None:
        """тест пути загрузки аватарки пользователя"""
        user = CustomUser.objects.create(username=TEST_USERNAME,
                                         first_name=TEST_FIRST_NAME,
                                         last_name=TEST_LAST_NAME,
                                         avatar=TEST_AVATAR_IMG_NAME)

        user.avatar = SimpleUploadedFile(TEST_AVATAR_IMG_NAME, b'', content_type='image/jpeg')
        user.save()
        self.assertIn(
            user.username + '/avatar/' + splitext(TEST_AVATAR_IMG_NAME)[0],
            user.avatar.name
        )

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT / TEST_USERNAME, ignore_errors=True)

