import os

from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton


class DetailGuidePage(BasePage):
    """Страница Руководства"""

    def __init__(self, test: FunctionalTest) -> None:
        super().__init__(test, reverse('guides:detail_guide', kwargs={'pk': 1}))  # установка адреса страницы,
                                                                                  # тестовый pk=1
