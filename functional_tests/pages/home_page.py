from django.urls import reverse

from functional_tests.pages.components.base_page import BasePage


class HomePage(BasePage):
    """Домашняя страница"""

    def __init__(self, test):
        super().__init__(test, '/')  # установка адреса страницы

