import os

from django.conf import settings
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, BaseButton


class NewArticlePage(BasePage):
    """Страница новой Статьи"""

    def __init__(self, test: FunctionalTest, guide_pk: int) -> None:
        # установка адреса страницы
        super().__init__(test, reverse('guides:new_article', kwargs={'guide_pk': guide_pk}))
        self.article_name_field = InputField(self._test, 'id_name')
        self.text_field = InputField(self._test, 'id_text')
        self.create_article_btn = SubmitButton(self._test)
