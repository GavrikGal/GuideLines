from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import BaseButton
from functional_tests.pages.components.panels import BasePanel


class DetailArticlePage(BasePage):
    """Страница Руководства"""

    def __init__(self, browser: WebDriver, live_server_url: str, guide_pk: int = 1, pk: int = 1) -> None:
        # установка адреса страницы, тестовый pk=1
        super().__init__(browser, live_server_url, reverse('guides:detail_article', kwargs={'guide_pk': guide_pk,
                                                                                            'pk': pk}))
        self.edit_article_btn = BaseButton(browser, id_="id_edit_article_btn")
        self.delete_article_btn = BaseButton(browser, id_="id_delete_article_btn")
        self.confirm_delete_article_btn = BaseButton(browser, id_='id_confirm_delete_article_btn')
        self.article_menu_btn = BaseButton(browser, id_='id_article_menu_btn')
        self.article_menu = BasePanel(browser, _panel_id='id_article_menu')
        self.modal_delete_panel = BasePanel(browser, _panel_id='id_modal_delete_panel')
        self.publish_btn = BaseButton(browser, id_="id_publish_btn")

    # @property
    # def guide_author(self) -> str:
    #     """Имя автора Руководства"""
    #     return self._browser.find_element(By.ID, 'guide').find_element(By.CLASS_NAME, 'card-footer').text
