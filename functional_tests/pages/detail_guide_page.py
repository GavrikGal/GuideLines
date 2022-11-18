from typing import Optional, TYPE_CHECKING
from django.urls import reverse
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import BaseButton

from functional_tests.base import FunctionalTest


class DetailGuidePage(BasePage):
    """Страница Руководства"""

    def __init__(self, test: FunctionalTest, pk: int = 1) -> None:
        # установка адреса страницы, тестовый pk=1
        super().__init__(test, reverse('guides:detail_guide', kwargs={'pk': pk}))
        self.edit_guide_btn = BaseButton(test, id_="id_edit_guide_btn")
        self.delete_guide_btn = BaseButton(test, id_="id_delete_guide_btn")
        self.confirm_delete_guide_btn = BaseButton(test, id_='id_confirm_delete_guide_btn')
        self.guide_menu_btn = BaseButton(test, id_='id_guide_menu_btn')
        self.guide_menu = self.BaseFadeInPanel(test, _panel_id='id_guide_menu')
        self.new_article_btn = BaseButton(self._test, id_='id_new_article_btn')
        self.modal_delete_panel = self.BaseFadeInPanel(test, _panel_id='id_modal_delete_panel')

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

    class BaseFadeInPanel(object):
        """Базовый класс для появляющихся панелей"""

        def __init__(self, test: FunctionalTest, _panel_id: str):
            self._browser = test.browser
            self._panel_id = _panel_id

        @property
        def _panel(self) -> Optional[WebElement]:
            """само меню"""
            try:
                return self._browser.find_element(By.ID, self._panel_id)
            except selenium.common.exceptions.NoSuchElementException:
                return None

        def is_displayed(self):
            """Меню видимо?"""
            if self._panel:
                return self._panel.is_displayed()
            else:
                return False

