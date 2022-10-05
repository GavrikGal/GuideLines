from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.buttons import LogoutButton, LoginButton


class BasePage(object):
    """Общие элементы для всех страниц"""

    def __init__(self, test: FunctionalTest, page_url: str = ''):
        self._test = test
        self._browser = test.browser
        self.page_url = page_url
        self.login_btn = LoginButton(self._test)
        self.logout_btn = LogoutButton(self._test)

    @property
    def page_title(self) -> str:
        """заголовок страницы"""
        page_title = self._browser.title
        return page_title

    @property
    def header(self) -> WebElement:
        """получить элемент шапки"""
        header = self._browser.find_element(By.ID, 'header')
        return header

    def go_to_page(self) -> 'BasePage':
        """перейти на страницу"""
        self._browser.get(self._test.live_server_url + self.page_url)
        # Подождать пока загрузится тайтл страницы
        self._test.assertIn(
            'GuideLines',
            self.page_title
        )
        return self
