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

        # и спокойно попадает на главную страницу
        # и видит слово GuideLines в тайтле страницы
        self.assertIn(
            'GuideLines',
            self.browser.title
        )

        # Это ли не счастье?
