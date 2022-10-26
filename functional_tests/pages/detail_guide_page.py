from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage


class DetailGuidePage(BasePage):
    """Страница Руководства"""

    def __init__(self, test: FunctionalTest) -> None:
        # установка адреса страницы, тестовый pk=1
        super().__init__(test, reverse('guides:detail_guide', kwargs={'pk': 1}))

    @property
    def guide_cover(self) -> WebElement:
        """Обложка Руководства"""
        return self._browser.find_element(By.ID, 'guide').find_element(By.TAG_NAME, 'img')

    def find_text(self, text) -> str:
        """Найти текст на странице"""
        return self._browser.find_element(By.XPATH, f"//*[text()='{text}']").text

    @property
    def guide_author(self) -> str:
        """Имя автора Руководства"""
        return self._browser.find_element(By.ID, 'guide').find_element(By.CLASS_NAME, 'card-footer').text
