from os.path import splitext, basename
from typing import Optional

from functional_tests.base import FunctionalTest
from functional_tests.pages.home_page import HomePage
from functional_tests.pages.new_guide_page import NewGuidePage
from functional_tests.pages.detail_guide_page import DetailGuidePage
from functional_tests.pages.edit_guide_page import EditGuidePage
from functional_tests.const import (
    TEST_LAST_NAME, TEST_GUIDE_NAME, TEST_FIRST_NAME,
    TEST_GUIDE_DESCRIPTION, TEST_GUIDE_COVER_IMG_PATH, TEST_GUIDE_NEW_COVER_IMG_PATH
)
from functional_tests.utils.services import create_user_guide_and_go_to_guide_page


class GuidesTest(FunctionalTest):
    """тесты Руководств"""

    def test_can_create_new_guide_without_cover_and_description(self) -> None:
        """тест: можно создать Руководство без обложки и описания"""

        # Гал создал руководство без обложки
        # Он сразу переходит на страницу Руководства
        create_user_guide_and_go_to_guide_page(self, cover_path=None, description=None)

    def test_can_edit_guide_without_cover_and_description(self) -> None:
        """тест: можно редактировать Руководство без обложки и описания"""

        # Гал создал руководство без обложки
        _, guide, _ = create_user_guide_and_go_to_guide_page(self, cover_path=None, description=None)

        # и посещает страницу редактирования Руководства
        edit_guide_page = EditGuidePage(self, guide.pk)
        edit_guide_page.go_to_page()

    def test_tooltip_with_bootstrap_javascript_work(self) -> None:
        """тест: всплывающая подсказка tooltip из script.js и bootstrap загружена и работает"""
        # Гал имеет созданное руководство
        # Он сразу переходит на страницу Руководства
        guide_page, _, _ = create_user_guide_and_go_to_guide_page(self)

        # Наводит мышку на кнопку добавления Сататьи
        guide_page.new_article_btn.hover()

        # И видит, что выскакивает подсказка. Это означает javascript отработал как надо
        self.assertTrue(
            guide_page.tooltip.is_displayed()
        )

    def test_can_create_new_guide(self) -> None:
        """тест можно создать новое руководство"""
        # Гал хочет создать свое первое Руководство.
        # Он зарегестрированный пользователь и залогиненый пользователь
        self.create_user_and_pre_authenticated_session()

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
        self.assertTrue(
            detail_guide_page.guide_cover.is_displayed()
        )
        self.assertIn(
            splitext(basename(TEST_GUIDE_COVER_IMG_PATH))[0],
            detail_guide_page.guide_cover.get_attribute('src')
        )

        # А на ней красуется название Руководства
        self.assertEqual(
            TEST_GUIDE_NAME,
            detail_guide_page.is_text_present(TEST_GUIDE_NAME)
        )
        # и описание
        self.assertEqual(
            TEST_GUIDE_DESCRIPTION,
            detail_guide_page.is_text_present(TEST_GUIDE_DESCRIPTION)
        )

        # И Гал видит, что автором руководства является он Сам. Красавчик!
        self.assertIn(
            TEST_FIRST_NAME,
            detail_guide_page.guide_author
        )
        self.assertIn(
            TEST_LAST_NAME,
            detail_guide_page.guide_author
        )

        # Кроме того, он видит заветную большую кнопку "Добавить статью"
        self.assertTrue(
            detail_guide_page.new_article_btn.is_displayed(),
            'Кнопка добавления Статьи не отображается'
        )

    def test_can_update_guide(self) -> None:
        """тест: можно редактировать свое Руководство"""

        # Гал хочет отредактировать свое первое Руководство.
        # Он сразу переходит на страницу Руководства
        guide_page, _, _ = create_user_guide_and_go_to_guide_page(self)

        self.assertIn(
            TEST_GUIDE_NAME,
            guide_page.page_title,
            'Невозможно зайти на страницу Руководства'
        )

        # На обложке Руководства Гал видит три точечки
        self.assertTrue(
            guide_page.guide_menu_btn.is_displayed(),
            'Не отображается кнопка меню Руководства'
        )

        # Он нажимает на них.
        guide_page.guide_menu_btn.click()
        # И вниз выпадает меню
        self.assertTrue(
            guide_page.guide_menu.is_displayed(),
            'Не отображается выпадающее меню Руководства'
        )

        # Гал находит там кнопку редактировать
        self.assertTrue(
            guide_page.edit_guide_btn.is_displayed(),
            'Не отображается кнопка редактирования'
        )

        # Нажимает
        guide_page.edit_guide_btn.click()

        # И попадает на страницу редактирования Руководства
        edit_guide_page = EditGuidePage(self)
        self.assertIn(
            'Редактировать',
            edit_guide_page.page_title,
            'Не переходит на страницу редактирования Руководства'
        )

        # Тут он видит поля Названия и Описания, в которых,
        # при создании руководства, были внесены данные
        self.assertTrue(
            edit_guide_page.guide_name_field.is_displayed(),
            'Поле Названия не отображается'
        )
        self.assertTrue(
            edit_guide_page.description_field.is_displayed(),
            'Поле Описания не отображается'
        )

        # Также видит кнопку выбора Обложки
        self.assertTrue(
            edit_guide_page.guide_cover_btn.is_displayed(),
            'Кнопка выбора Обложки не отображается'
        )

        # Для начала он пробует обновить все данные во внесенных им ранее полях (Название, Описание, Обложка)
        edit_guide_page.guide_name_field.send_keys('Обновленное ' + TEST_GUIDE_NAME)
        edit_guide_page.description_field.send_keys('Обновленное описание' + TEST_GUIDE_DESCRIPTION)
        edit_guide_page.set_cover_img(TEST_GUIDE_NEW_COVER_IMG_PATH)

        # Находит кнопку "Сохранить".
        self.assertTrue(
            edit_guide_page.save_guide_btn.is_displayed(),
            'Кнопка Сохранить не отображается'
        )
        # И жмет её
        edit_guide_page.save_guide_btn.click()

        # Страница обновляется и он возвращается на страницу детального просмотра Руководства
        self.assertIn(
            'Обновленное ' + TEST_GUIDE_NAME,
            guide_page.page_title,
            'Невозможно зайти на страницу Руководства'
        )

    def test_can_delete_guide(self) -> None:
        """Тест можно удалить Руководство"""

        # Гал имеет написанное руководство, но он не хочет чтобы оно было, а хочет его удалить
        # Сразу переходит на страницу Руководства
        guide_page, _, _ = create_user_guide_and_go_to_guide_page(self)

        # Нажимает на кнопку с тремя точками
        guide_page.guide_menu_btn.click()

        # Выпадает меню
        self.assertTrue(
            guide_page.guide_menu.is_displayed(),
            "Нет выпадающего меню на Руководстве"
        )

        # В этом меню есть кнопка Удалить
        self.assertTrue(
            guide_page.delete_guide_btn.is_displayed(),
            "Нет кнопки удаления Руководства"
        )

        # Гал нажимает на кнопку
        guide_page.delete_guide_btn.click()

        # Появляется модальное окно, где надо подтвердить своё намерение
        self.assertTrue(
            guide_page.modal_delete_panel.is_displayed(),
            'Нет модального окна подтверждения удаления Руководства'
        )
        self.assertTrue(
            guide_page.confirm_delete_guide_btn.is_displayed(),
            'Нет кнопки подтверждающей удаление Руководства'
        )

        # Гал нажимает кнопку удалить в модальном окне
        guide_page.confirm_delete_guide_btn.click()

        # Его перекидывает на главную страницу
        home_page = HomePage(self)
        self.assertIn(
            'Главная',
            home_page.page_title,
            'Не перекинуло на главную страницу'
        )

        # Больше гал не может зайти на страницу удаленного Руководства
        self.assertNotIn(
            TEST_GUIDE_NAME,
            guide_page.page_title,
            'Руководство не удалено. Всё еще можно зайти на страницу Руководства'
        )
