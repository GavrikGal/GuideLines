import os

from django.conf import settings
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, BaseButton


class NewGuidePage(BasePage):
    """Страница нового Руководства"""

    def __init__(self, test: FunctionalTest) -> None:
        super().__init__(test, reverse('guides:new_guide'))  # установка адреса страницы
        self.guide_name_field = InputField(self._test, 'id_name')
        self.description_field = InputField(self._test, 'id_description')
        self.create_guide_btn = SubmitButton(self._test)
        self.guide_cover_btn = BaseButton(self._test, id_='id_cover')

    def set_cover_img(self, img_path: str) -> None:
        """Установка картинки обложки Руководства"""
        self.guide_cover_btn.send_keys(str(settings.BASE_DIR / img_path))
