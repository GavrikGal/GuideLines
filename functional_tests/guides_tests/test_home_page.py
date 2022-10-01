import time

from selenium.webdriver.common.by import By
from functional_tests.base import FunctionalTest


class HomePageTest(FunctionalTest):
    """тест главной страницы"""

    def test_can_open_home_page(self):
        """тест можно открыть главную страницу"""
        # Гал хочет открыть главную страницу системы.
        # Он вводит адрес
        self.browser.get(self.live_server_url)

        print(self.live_server_url)

        # и спокойно попадает на главную страницу
        # на которой видит название лаборатории
        title = self.browser.find_element(By.TAG_NAME, 'title')
        time.sleep(3)
        self.assertIn(
            'GuideLines',
            title.text
        )
