from django.urls import reverse
from selenium.webdriver.common.by import By

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, LogoutButton


class LoginPage(BasePage):
    """Домашняя страница"""

    def __init__(self, test):
        super().__init__(test, reverse('login'))  # установка адреса страницы
        self.login_field = InputField(self.test, 'id_username')
        self.password_field = InputField(self.test, 'id_password')
        self.login_to_system_btn = SubmitButton(self.test)

    # @property
    # def popup_error_message(self):
    #     """всплывающее сообщение об ошибке"""
    #     return self.test.browser.find_element(By.CSS_SELECTOR, '.alert-danger')
