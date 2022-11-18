from selenium.webdriver.firefox.webdriver import WebDriver

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import BaseButton


class HomePage(BasePage):
    """Домашняя страница"""

    def __init__(self, browser: WebDriver, live_server_url: str) -> None:
        super().__init__(browser, live_server_url, '/')  # установка адреса страницы
        self.new_guide_btn = BaseButton(self._browser, name="new_guide_btn")
