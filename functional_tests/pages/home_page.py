from django.urls import reverse

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import LogoutButton, LoginButton


class HomePage(BasePage):
    """Домашняя страница"""

    def __init__(self, test):
        super().__init__(test, '/')  # установка адреса страницы
        self.login_btn = LoginButton(self.test)
        self.logout_btn = LogoutButton(self.test)
