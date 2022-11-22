from django.conf import settings
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, BaseButton


class EditArticlePage(BasePage):
    """Страница редактирования Статьи"""

    def __init__(self, browser: WebDriver, live_server_url: str, guide_pk: int = 1, pk: int = 1) -> None:
        # установка адреса страницы, тестовый pk=1
        super().__init__(browser, live_server_url, reverse('guides:edit_article', kwargs={'guide_pk': guide_pk,
                                                                                          'pk': pk}))
        self.article_name_field = InputField(browser, 'id_name')
        self.text_field = InputField(browser, 'id_text')
        self.save_article_btn = SubmitButton(browser)
