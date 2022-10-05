from django.urls import reverse

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, BaseButton


class LoginPage(BasePage):
    """Домашняя страница"""

    def __init__(self, test: FunctionalTest):
        super().__init__(test, reverse('login'))  # установка адреса страницы
        self.login_field = InputField(self._test, 'id_username')
        self.password_field = InputField(self._test, 'id_password')
        self.login_to_system_btn = SubmitButton(self._test)
        self.registration_btn = BaseButton(self._test, id_='id_registration_btn')

    # @property
    # def popup_error_message(self):
    #     """всплывающее сообщение об ошибке"""
    #     return self.test.browser.find_element(By.CSS_SELECTOR, '.alert-danger')
