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
        registration_page = RegistrationPage(self)
        registration_page.go_to_page()

        # На ней видит поля для ввода логина
        self.assertTrue(
            registration_page.login_field.is_displayed()
        )

        # Имени и фамилии
        self.assertTrue(
            registration_page.first_name_field.is_displayed()
        )
        self.assertTrue(
            registration_page.last_name_field.is_displayed()
        )

        # Пароля и подтверждения пароля
        self.assertTrue(
            registration_page.password_field.is_displayed()
        )
        self.assertTrue(
            registration_page.confirm_password_field.is_displayed()
        )

        # А также кнопку добавления аватара
        self.assertTrue(
            registration_page.avatar_btn.is_displayed()
        )

        # Так же имеется кнопка регистрации
        self.assertTrue(
            registration_page.registration_to_system_btn.is_displayed()
        )

        # Гал заполняет все данные
        registration_page.login_field.send_keys('Test_Login')
        registration_page.first_name_field.send_keys('Test_Gavrik')
        registration_page.last_name_field.send_keys('Test_Gal')
        registration_page.password_field.send_keys('Test_Password12')
        registration_page.confirm_password_field.send_keys('Test_Password12')
        registration_page.set_avatar_img(r'\functional_tests\img\avatar.jpg')
        registration_page.registration_to_system_btn.click()



        # Нажимает кнопку регистрации

        # Его редиректит на главную страницу

        # Где он может выполнить вход систему
        # нажав на кнопку "вход"

        # Так он перейдет на страницу логина

        # Где введя логин и пароль, и нажав "вход"

        # Он становится аутенцифицированным пользователем
        # Что подтверждает наличие его имени и фамилии в шапке

        self.fail('Доделать')