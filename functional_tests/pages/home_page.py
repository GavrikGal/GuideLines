from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import BaseButton


class HomePage(BasePage):
    """Домашняя страница"""

    def __init__(self, browser: WebDriver, live_server_url: str) -> None:
        super().__init__(browser, live_server_url, '/')  # установка адреса страницы
        self.new_guide_btn = BaseButton(self._browser, name="new_guide_btn")

    def get_guide(self, pk: int) -> WebElement:
        """Руководство с соответствующим pk"""
        return self._browser.find_element(By.ID, f'id_guide_{pk}')

    def get_guide_cover_img(self, pk: int) -> WebElement:
        """Картинка обложки Руководства"""
        return self._browser.find_element(By.ID, f'id_guide_{pk}').find_element(By.TAG_NAME, 'img')

    def get_guide_author(self, pk: int) -> str:
        """Имя автора Руководства"""
        return self._browser.find_element(By.ID, f'id_guide_{pk}').find_element(By.CLASS_NAME, 'card-footer').text
