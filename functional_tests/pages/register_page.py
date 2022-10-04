from django.urls import reverse
from selenium.webdriver.common.by import By

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, LogoutButton


class RegisterPage(BasePage):
    """Домашняя страница"""

    def __init__(self, test):
        super().__init__(test, reverse('account/register'))  # установка адреса страницы
        self.login_field = InputField(self.test, 'id_username')
        self.first_name_field = InputField(self.test, 'id_firstname')
        self.last_name_field = InputField(self.test, 'id_lastname')
        self.password_field = InputField(self.test, 'id_password')
        self.confirm_password_field = InputField(self.test, 'id_confirm_password')
        self.register_to_system_btn = SubmitButton(self.test)

    # @property
    # def popup_error_message(self):
    #     """всплывающее сообщение об ошибке"""
    #     return self.test.browser.find_element(By.CSS_SELECTOR, '.alert-danger')
