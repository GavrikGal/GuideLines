import time
from django.contrib.auth.models import User

from functional_tests.base import FunctionalTest
from functional_tests.pages.home_page import HomePage
from functional_tests.pages.new_guide_page import NewGuidePage
from functional_tests.pages.detail_guide_page import DetailGuidePage

TEST_GUIDE_NAME = 'Моё новое Руководство'
TEST_GUIDE_DESCRIPTION = 'Это Руководство замечательно отражает всё то, что мы хотим показать. Это будет ' \
                         'увлекательное руководство. Главное, чтобы в описании было бы много строк, а то не ' \
                         'получится нормально протоестировать это описание. Я думаю этого должно хватить. Но, ' \
                         'на всякий случай, пусть будет еще пару слов. Пара слов."'
TEST_GUIDE_COVER_IMG_PATH = r'\functional_tests\img\Cover.jpg'


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
        self.assertTrue(
            home_page.new_guide_btn.is_displayed()
        )

        # Нажимает на нее
        home_page.new_guide_btn.click()

        # Попадает на страницу создания нового Руководства
        new_guide_page = NewGuidePage(self)
        self.assertIn(
            "Новое Руководство",
            new_guide_page.page_title
        )

        # Где он может ввести название руководства
        self.assertTrue(
            new_guide_page.guide_name_field.is_displayed()
        )

        # Описание руководства
        self.assertTrue(
            new_guide_page.description_field
        )

        # Видит кнопку выбора обложки руководства
        self.assertTrue(
            new_guide_page.guide_cover_btn.is_displayed()
        )

        # Он заполняет соответствующие поля
        new_guide_page.guide_name_field.send_keys(TEST_GUIDE_NAME)
        new_guide_page.description_field.send_keys(TEST_GUIDE_DESCRIPTION)

        # Устатавливает фон
        new_guide_page.set_cover_img(TEST_GUIDE_COVER_IMG_PATH)

        # Нажимает кнопку "Создать Руководство"
        new_guide_page.create_guide_btn.click()

        # И его чудесным образом переносит на страницу
        # только что созданного Руководста
        detail_guide_page = DetailGuidePage(self)
        self.assertIn(
            TEST_GUIDE_NAME,
            detail_guide_page.page_title
        )

        # Где он видит загруженную им обложку

        # А на ней красуется название Руководства
        # и описание

        # И Гал видит, что автором руководства является он Сам. Красавчик!

        self.fail("Доделать")



