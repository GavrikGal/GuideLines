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
        # Он зарегестрированный пользователь и залогиненый пользователь
        self.create_pre_authenticated_session(username='Gal', first_name='Дмитрий', last_name='Гал')

        # Он открывает главную страницу
        home_page = HomePage(self)
        home_page.go_to_page()

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



