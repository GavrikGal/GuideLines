import time

from functional_tests.base import FunctionalTest
from functional_tests.pages.login_page import LoginPage
from functional_tests.pages.registration_page import RegistrationPage


class RegistrationTest(FunctionalTest):
    """Тесты регистрации"""

    def test_can_open_registration_page(self) -> None:
        """Можно перейти на страницу регистрации"""

        # Гал открывает страницу логина
        login_page = LoginPage(self)
        login_page.go_to_page()

        # И видит там кнопку "зарегистрироваваться"
        self.assertTrue(
            login_page.registration_btn.is_displayed()
        )

        # Нажимает ее
        login_page.registration_btn.click()

        # И попадает на страницу регистрации нового пользователя
        registration_page = RegistrationPage(self)
        self.assertIn(
            'Регистрация',
            registration_page.page_title
        )

    def test_can_be_registered(self) -> None:
        """Можно зарегистрироваться в системе"""

        # Гал открывает страницу регистрации

        # На ней видит поля для ввода логина

        # Имени и фамилии

        # Пароля и подтверждения пароля

        # А также кнопку добавления аватара

        # Так же имеется кнопка регистрации

        # Гал заполняет все данные

        # Нажимает кнопку регистрации

        # Его редиректит на главную страницу

        # Где он может выполнить вход систему
        # нажав на кнопку "вход"

        # Так он перейдет на страницу логина

        # Где введя логин и пароль, и нажав "вход"

        # Он становится аутенцифицированным пользователем
        # Что подтверждает наличие его имени и фамилии в шапке

