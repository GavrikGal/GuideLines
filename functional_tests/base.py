import os
from datetime import datetime
from shutil import rmtree

from django.test.testcases import LiveServerThread, QuietWSGIRequestHandler
from django.core.servers.basehttp import WSGIServer

from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from django.conf import settings

import time

from functional_tests.utils.const import (
    TEST_USERNAME
)


MAX_WAIT = 3
SCREEN_DUMP_LOCATION = settings.BASE_DIR / 'logs' / 'screendumps'


class LiveServerSingleThread(LiveServerThread):
    """Runs a single threaded server rather than multi threaded. Reverts https://github.com/django/django/pull/7832"""

    def _create_server(self):

        """
        the keep-alive fixes introduced in Django 2.1.4 (934acf1126995f6e6ccba5947ec8f7561633c27f)
        cause problems when serving the static files in a stream.
        We disable the helper handle method that calls handle_one_request multiple times.
        """
        QuietWSGIRequestHandler.handle = QuietWSGIRequestHandler.handle_one_request

        return WSGIServer((self.host, self.port), QuietWSGIRequestHandler, allow_reuse_address=False)


class LiveServerSingleThreadedTestCase(LiveServerTestCase):
    "A thin sub-class which only sets the single-threaded server as a class"
    server_thread_class = LiveServerSingleThread


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


# class FunctionalTest(StaticLiveServerTestCase):
class FunctionalTest(LiveServerSingleThreadedTestCase):
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
        # options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        options.binary_location = r'/usr/bin/firefox'
        self.used_headless_driver = os.environ.get("HEADLESS_DRIVER", False)
        if self.used_headless_driver:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        self.browser = webdriver.Firefox(options=options)
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
