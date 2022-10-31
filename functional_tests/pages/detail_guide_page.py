from typing import Optional
from django.urls import reverse
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import BaseButton


class DetailGuidePage(BasePage):
    """Страница Руководства"""

    def __init__(self, test: FunctionalTest, pk: int = 1) -> None:
        # установка адреса страницы, тестовый pk=1
        super().__init__(test, reverse('guides:detail_guide', kwargs={'pk': pk}))
        self.edit_guide_btn = BaseButton(test, id_="id_edit_guide_btn")
        self.guide_menu_btn = BaseButton(test, id_='id_guide_menu_btn')
        self.guide_menu = self.BaseDropDownMenu(test, _menu_id='id_guide_menu')

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

    class BaseDropDownMenu(object):
        """Базовый класс для выпадающих меню"""

        def __init__(self, test: FunctionalTest, _menu_id: str):
            self._browser = test.browser
            self._menu_id = _menu_id

        @property
        def _menu(self) -> Optional[WebElement]:
            """само меню"""
            try:
                return self._browser.find_element(By.ID, self._menu_id)
            except selenium.common.exceptions.NoSuchElementException:
                return None

        def is_displayed(self):
            """Меню видимо?"""
            if self._menu:
                return self._menu.is_displayed()
            else:
                return False

