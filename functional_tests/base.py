import os
from datetime import datetime
from shutil import rmtree
from typing import Optional

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from django.conf import settings
from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY,
    get_user_model
)
from django.contrib.auth.models import User
import time

from functional_tests.const import (
    TEST_USERNAME, TEST_LAST_NAME, TEST_FIRST_NAME, TEST_PASSWORD,
    TEST_GUIDE_NAME, TEST_GUIDE_DESCRIPTION, TEST_GUIDE_COVER_IMG_PATH,
)

from guides.models import Guide

MAX_WAIT = 3
SCREEN_DUMP_LOCATION = settings.BASE_DIR / 'logs' / 'screendumps'


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.2)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """базовый функциональный тест"""

    @classmethod
    def setUpClass(cls) -> None:
        # Установка порта на котором будет проводится тестирование из переменных окружения TEST_SERVER_PORT=15051
        if os.environ.get("TEST_SERVER_PORT"):
            cls.port = int(os.environ.get("TEST_SERVER_PORT"))
        super().setUpClass()

    def setUp(self) -> None:
        """Установка параметров тестовой среды"""
        options = Options()
        # использовать для тестов драйвер без окна или с окном
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.used_headless_driver = os.environ.get("HEADLESS_DRIVER", False)
        if self.used_headless_driver:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        self.browser = webdriver.Firefox(options=options)
        self.user = None
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self) -> None:
        """демонтаж"""
        if self.used_headless_driver:
            if self._test_has_failed():
                if not os.path.exists(SCREEN_DUMP_LOCATION):
                    os.makedirs(SCREEN_DUMP_LOCATION)
                for ix, handle in enumerate(self.browser.window_handles):
                    self._windowid = ix
                    self.browser.switch_to.window(handle)
                    self.take_screenshot()
                    self.dump_html()
        self.browser.quit()
        rmtree(settings.MEDIA_ROOT / TEST_USERNAME, ignore_errors=True)
        super().tearDown()

    def _test_has_failed(self):
        """тест не сработал"""
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self) -> None:
        """взять снимок экрана"""
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self) -> None:
        """выгрузить html"""
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self) -> str:
        """получить имя файла"""
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    @wait
    def wait_for(self, fn):
        """ожидать"""
        return fn()

    @staticmethod
    def create_user(username: str = TEST_USERNAME, password: str = TEST_PASSWORD,
                    first_name: str = TEST_FIRST_NAME, last_name: str = TEST_LAST_NAME,
                    is_superuser: bool = False) -> User:
        """
        Создать пользователя.
           Все аргументы могут быть опущены. Что приведет к созданию тестового пользователя по-умолчанию
        """
        user_model = get_user_model()
        user = user_model.objects.create(username=username,
                                         first_name=first_name,
                                         last_name=last_name
                                         )
        user.set_password(password)
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_user_and_pre_authenticated_session(self, username: str = TEST_USERNAME,
                                                  password: str = TEST_PASSWORD,
                                                  first_name: str = TEST_FIRST_NAME,
                                                  last_name: str = TEST_LAST_NAME, ) -> User:
        """
        Создать пользователя и аутентифицированную сессию
            Все аргументы могут быть опущены. Что приведет к созданию тестового пользователя по-умолчанию
        """
        # First, create a new test user
        user = self.create_user(username, password, first_name, last_name)

        # Then create the authenticated session using the new user credentials
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        self.user = user

        self.browser.get(self.live_server_url + '/404_no_such_url/')

        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'secure': False,
            'path': '/',
        }

        self.browser.add_cookie(cookie)

        return user

    def create_guide(self, author: User, name: str = TEST_GUIDE_NAME,
                     description: Optional[str] = TEST_GUIDE_DESCRIPTION,
                     cover_path: Optional[str] = TEST_GUIDE_COVER_IMG_PATH) -> Guide:
        """Создает Руководство с автором author, названием name, описанием description и обложкой, расположенной
        по пути cover_path. Если не задавать параметры name, description, cover_path, то будут испозованы тестовые
        значения поумолчанию"""
        guide = Guide.objects.create(name=name,
                                     description=description,
                                     author=author)
        if cover_path:
            guide.cover = SimpleUploadedFile(cover_path,
                                             content=open(settings.BASE_DIR / cover_path, 'rb').read(),
                                             content_type='image/jpeg')
            guide.save()
        return guide
