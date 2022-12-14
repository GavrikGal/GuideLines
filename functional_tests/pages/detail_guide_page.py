from collections import defaultdict
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from typing import Optional, DefaultDict

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import BaseButton
from functional_tests.pages.components.panels import BasePanel
from functional_tests.pages.components.cards import BaseCard


class DetailGuidePage(BasePage):
    """Страница Руководства"""

    def __init__(self, browser: WebDriver, live_server_url: str, pk: int = 1) -> None:
        # установка адреса страницы, тестовый pk=1
        super().__init__(browser, live_server_url, reverse('guides:detail_guide', kwargs={'guide_pk': pk}))
        self.edit_guide_btn = BaseButton(browser, id_="id_edit_guide_btn")
        self.delete_guide_btn = BaseButton(browser, id_="id_delete_guide_btn")
        self.confirm_delete_guide_btn = BaseButton(browser, id_='id_confirm_delete_guide_btn')
        self.guide_menu_btn = BaseButton(browser, id_='id_guide_menu_btn')
        self.guide_menu = BasePanel(browser, _panel_id='id_guide_menu')
        self.new_article_btn = BaseButton(browser, id_='id_new_article_btn')
        self.modal_delete_panel = BasePanel(browser, _panel_id='id_modal_delete_panel')
        self.article_cards: DefaultDict[str, BaseCard] = defaultdict()

    @property
    def guide_cover(self) -> WebElement:
        """Обложка Руководства"""
        return self._browser.find_element(By.ID, 'guide').find_element(By.TAG_NAME, 'img')

    @property
    def guide_author(self) -> str:
        """Имя автора Руководства"""
        return self._browser.find_element(By.ID, 'guide').find_element(By.CLASS_NAME, 'card-footer').text

    def get_article(self, pk: int) -> Optional[BaseCard]:
        """Вернет Статью с соответствующим pk"""
        id_article = f'id_article_{pk}'
        if id_article not in self.article_cards:
            self.article_cards[id_article] = BaseCard(browser=self._browser, card_id=id_article)
        return self.article_cards.get(id_article)
