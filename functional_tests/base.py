import os
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from django.conf import settings
from django.contrib.auth import get_user_model
import time


MAX_WAIT = 3
SCREEN_DUMP_LOCATION = settings.BASE_DIR / 'logs' / 'screendumps'
User = get_user_model()


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
    def setUpClass(cls):
        if os.environ.get("TEST_SERVER_PORT"):
            cls.port = int(os.environ.get("TEST_SERVER_PORT"))
        super().setUpClass()

    def setUp(self):
        """установка"""
        options = Options()
        # использовать для тестов драйвер без окна или с окном
        self.used_headless_driver = os.environ.get("HEADLESS_DRIVER", False)
        if self.used_headless_driver:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        self.browser = webdriver.Firefox(options=options)
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self):
        """демонтаж"""
        if self.used_headless_driver:
            if self._test_has_failed():
                if not os.path.exists(SCREEN_DUMP_LOCATION):
                    os.makedirs(SCREEN_DUMP_LOCATION)
                for ix, handle in enumerate(self.browser.window_handles):
                    self._windowid = ix
                    self.browser.switch_to_window(handle)
                    self.take_screenshot()
                    self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        """тест не сработал"""
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        """взять снимок экрана"""
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        """выгрузить html"""
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
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
    def create_user(username='Test_user', password='Password12',
                    first_name='Test_First_Name', last_name='Test_Last_name',
                    email='test.dmitry.gal@gmail.com', is_superuser=False) -> 'User':
        """
        Создать пользователя.
           Все аргументы могут быть опущены. Что приведет к созданию тестового пользователя по-умолчанию
        """
        user = User.objects.create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   email=email)
        user.set_password(password)
        user.is_superuser = is_superuser
        user.save()
        return user
