import os

from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton


class RegistrationPage(BasePage):
    """Страница регистрации"""

    def __init__(self, test: FunctionalTest) -> None:
        super().__init__(test, reverse('guides:registration'))  # установка адреса страницы
        self.login_field = InputField(self._test, 'id_username')
        self.first_name_field = InputField(self._test, 'id_first_name')
        self.last_name_field = InputField(self._test, 'id_last_name')
        self.password_field = InputField(self._test, 'id_password1')
        self.confirm_password_field = InputField(self._test, 'id_password2')
        self.registration_to_system_btn = SubmitButton(self._test)

    @property
    def avatar_btn(self) -> WebElement:
        """Кнопка выбора аватара"""
        return self._browser.find_element(By.ID, 'id_avatar')

    def set_avatar_img(self, img_path: str) -> None:
        """Установка картинки аватара"""
        self.avatar_btn.send_keys(os.getcwd() + img_path)
