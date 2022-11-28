from functional_tests.base import FunctionalTest
from functional_tests.pages.login_page import LoginPage
from functional_tests.pages.home_page import HomePage

from functional_tests.utils.services import create_user


class LoginTest(FunctionalTest):
    """тест входа в систему"""

    def test_can_login_and_logout(self) -> None:
        """Можно войти в систему и выйти из нее"""

        # Гал когда-то уже регался в системе Обноволено
        user = create_user(username='Gal', password='Password123')

        # Гал заходит на страницу логина
        login_page = LoginPage(self.browser, self.live_server_url)
        login_page.go_to_page()
        self.assertIn(
            'Вход',
            login_page.page_title
        )

        # На ней он видит поля для ввода логина и пароля
        login_field = login_page.login_field
        password_field = login_page.password_field

        # Гал вводит логин и пароль
        # и нажимает кнопку войти
        login_field.send_keys(user.username)
        password_field.send_keys('Password123')
        login_page.login_to_system_btn.click()

        # Гал редиректится на главную страницу
        home_page = HomePage(self.browser, self.live_server_url)
        self.assertIn(
            'Главная',
            home_page.page_title
        )
        # и видит, что в навигационной панельке красуется его имя и фамилия
        self.assertIn(
            user.first_name,
            home_page.header.text
        )
        self.assertIn(
            user.last_name,
            home_page.header.text
        )

        # Также рядом есть кнопка выход
        self.assertTrue(
            home_page.logout_btn.is_displayed()
        )

        # Гал нажимает на нее
        home_page.logout_btn.click()

        # И видит, что его имя и фамилия пропали, и он опять может войти в систему
        self.assertNotIn(
            user.first_name,
            home_page.header.text
        )
        self.assertNotIn(
            user.last_name,
            home_page.header.text
        )
        self.assertTrue(
            home_page.login_btn.is_displayed()
        )
