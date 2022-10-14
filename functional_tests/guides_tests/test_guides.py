import time
from django.contrib.auth.models import User

from functional_tests.base import FunctionalTest
from functional_tests.pages.home_page import HomePage
from guides.models import CustomUser


class GuidesTest(FunctionalTest):
    """тесты Руководств"""

    def test_can_create_new_guide(self) -> None:
        """тест можно создать новое руководство"""
        # Гал хочет создать свое первое Руководство.
        # Он зарегестрированный пользователь
        user = self.create_user(username='Gal', password='Password123')

        # и залогиненый пользователь
        # todo: реализовать вход в тесте с помощью cookies

        response = self.client.post('/account/login/', {'username': 'Gal', 'password': 'Password123'})
        # print(self.client.login(username='Gal', password='Password123'))
        cookies = self.client.cookies
        print(cookies)

        self.browser.add_cookie({'/': cookies})

        # Он открывает главную страницу
        home_page = HomePage(self)
        home_page.go_to_page()
        time.sleep(5)

        # Находит кнопку добавления нового руководства

        # Нажимает на нее

        # Попадает на страницу создания нового Руководства

        # Где он может ввести название руководства

        # Описание руководства

        # Обложку руководства

        # Он заполняет соответствующие поля

        # Устатавливает фон

        # Нажимает кнопку "Создать Руководство"

        # И его чудесным образом переносит на страницу
        # только что созданного Руководста

        # Где он видит загруженную им обложку

        # А на ней красуется название Руководства
        # и описание

        self.fail("Доделать")



