from django.urls import reverse
from selenium.webdriver.firefox.webdriver import WebDriver

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, BaseButton


class LoginPage(BasePage):
    """Домашняя страница"""

    def __init__(self, browser: WebDriver, live_server_url: str) -> None:
        super().__init__(browser, live_server_url, reverse('login'))  # установка адреса страницы
        self.login_field = InputField(browser, 'id_username')
        self.password_field = InputField(browser, 'id_password')
        self.login_to_system_btn = SubmitButton(browser)
        self.registration_btn = BaseButton(browser, id_='id_registration_btn')

    # @property
    # def popup_error_message(self):
    #     """всплывающее сообщение об ошибке"""
    #     return self.test.browser.find_element(By.CSS_SELECTOR, '.alert-danger')
