from functional_tests.base import FunctionalTest
from functional_tests.pages.registration_page import RegistrationPage
from functional_tests.pages.login_page import LoginPage
from functional_tests.pages.home_page import HomePage
from functional_tests.utils.const import (
    TEST_USERNAME, TEST_LAST_NAME, TEST_FIRST_NAME, TEST_PASSWORD, TEST_AVATAR_IMG_PATH
)


class RegistrationTest(FunctionalTest):
    """Тесты регистрации"""

    def test_can_open_registration_page(self) -> None:
        """Можно перейти на страницу регистрации"""

        # Гал открывает страницу логина
        login_page = LoginPage(self.browser, self.live_server_url)
        login_page.go_to_page()

        # И видит там кнопку "зарегистрироваваться"
        self.assertTrue(
            login_page.registration_btn.is_displayed()
        )

        # Нажимает ее
        login_page.registration_btn.click()

        # И попадает на страницу регистрации нового пользователя
        registration_page = RegistrationPage(self.browser, self.live_server_url)
        self.assertIn(
            'Регистрация',
            registration_page.page_title
        )

    def test_can_be_registered(self) -> None:
        """Можно зарегистрироваться в системе"""

        # Гал открывает страницу регистрации
        registration_page = RegistrationPage(self.browser, self.live_server_url)
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
        registration_page.login_field.send_keys(TEST_USERNAME)
        registration_page.first_name_field.send_keys(TEST_FIRST_NAME)
        registration_page.last_name_field.send_keys(TEST_LAST_NAME)
        registration_page.password_field.send_keys(TEST_PASSWORD)
        registration_page.confirm_password_field.send_keys(TEST_PASSWORD)
        registration_page.set_avatar_img(TEST_AVATAR_IMG_PATH)

        # Нажимает кнопку регистрации
        self.browser.set_window_size(1920, 1080)    # Фикс недостаточной высоты окна
        registration_page.registration_to_system_btn.click()

        # Его редиректит на главную страницу
        home_page = HomePage(self.browser, self.live_server_url)
        self.assertTrue(
            'Главная',
            home_page.page_title
        )

        # Теперь он может выполнить вход систему
        # Так он перейдет на страницу логина
        login_page = LoginPage(self.browser, self.live_server_url)
        login_page.go_to_page()

        # Где введя логин и пароль, и нажав "вход"
        login_page.login_field.send_keys(TEST_USERNAME)
        login_page.password_field.send_keys(TEST_PASSWORD)
        login_page.login_to_system_btn.click()

        # Он становится аутенцифицированным пользователем
        # Что подтверждает наличие его имени и фамилии в шапке
        self.assertIn(
            TEST_FIRST_NAME,
            login_page.header.text
        )
