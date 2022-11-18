from django.urls import reverse
from selenium.webdriver.firefox.webdriver import WebDriver

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton


class NewArticlePage(BasePage):
    """Страница новой Статьи"""

    def __init__(self, browser: WebDriver, live_server_url: str, guide_pk: int) -> None:
        # установка адреса страницы
        super().__init__(browser, live_server_url, reverse('guides:new_article', kwargs={'guide_pk': guide_pk}))
        self.article_name_field = InputField(browser, 'id_name')
        self.text_field = InputField(browser, 'id_text')
        self.create_article_btn = SubmitButton(browser)
