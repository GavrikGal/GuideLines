import os

from django.urls import reverse
from selenium.webdriver.common.by import By

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton


class RegistrationPage(BasePage):
    """Страница регистрации"""

    def __init__(self, test):
        super().__init__(test, reverse('registration'))  # установка адреса страницы
        self.login_field = InputField(self.test, 'id_username')
        self.first_name_field = InputField(self.test, 'id_firstname')
        self.last_name_field = InputField(self.test, 'id_lastname')
        self.email_field = InputField(self.test, 'id_email')
        self.password_field = InputField(self.test, 'id_password')
        self.confirm_password_field = InputField(self.test, 'id_confirm_password')
        self.registration_to_system_btn = SubmitButton(self.test)

    @property
    def avatar_btn(self):
        """Кнопка выбора аватара"""
        return self.test.browser.find_element(By.ID, 'id_avatar_btn')

    def set_avatar_img(self, img_path):
        """Установка картинки аватара"""
        return self.avatar_btn.send_keys(os.getcwd() + img_path)
