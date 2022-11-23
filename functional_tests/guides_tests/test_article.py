import time
from django.urls import reverse

from functional_tests.base import FunctionalTest
from functional_tests.pages.detail_guide_page import DetailGuidePage
from functional_tests.pages.new_article_page import NewArticlePage
from functional_tests.pages.detail_article_page import DetailArticlePage
from functional_tests.pages.edit_article_page import EditArticlePage
from functional_tests.const import (TEST_ARTICLE_NAME, TEST_ARTICLE_TEXT)
from functional_tests.utils.services import (
    create_user_guide_and_go_to_guide_page,
    create_user_guide_article_then_go_to_article_page,
    create_article
)


class ArticleTest(FunctionalTest):
    """тесты Статей"""

    def test_can_delete_article(self) -> None:
        """Тест можно удалить Статью"""

        # Гал имеет написанную статью, но он не хочет чтобы она была, а хочет её удалить
        # Сразу переходит на страницу Статьи
        article_page, guide, _, article = create_user_guide_article_then_go_to_article_page(
            self.browser, self.live_server_url
        )

        # Нажимает на кнопку с тремя точками
        article_page.article_menu_btn.click()

        # Выпадает меню
        self.assertTrue(
            article_page.article_menu.is_displayed(),
            "Нет выпадающего меню на странице Статьи"
        )

        # В этом меню есть кнопка Удалить
        self.assertTrue(
            article_page.delete_article_btn.is_displayed(),
            "Нет кнопки удаления Статьи"
        )

        # Гал нажимает на кнопку
        article_page.delete_article_btn.click()

        # Появляется модальное окно, где надо подтвердить своё намерение
        self.assertTrue(
            article_page.modal_delete_panel.is_displayed(),
            'Нет модального окна подтверждения удаления Статьи'
        )
        self.assertTrue(
            article_page.confirm_delete_article_btn.is_displayed(),
            'Нет кнопки подтверждающей удаление Статьи'
        )

        # Гал нажимает кнопку удалить в модальном окне
        article_page.confirm_delete_article_btn.click()

        # Его перекидывает на главную страницу
        guide_page = DetailGuidePage(self.browser, self.live_server_url)
        self.assertIn(
            guide.name,
            guide_page.page_title,
            'Не перекинуло на страницу Руководства'
        )

        # Больше гал не может зайти на страницу удаленного Руководства
        self.browser.get(
            self.live_server_url +
            reverse('guides:detail_article', kwargs={'guide_pk': guide.pk,
                                                     'pk': article.pk}))
        self.assertNotIn(
            TEST_ARTICLE_NAME,
            article_page.page_title,
            'Статья не удалена. Всё еще можно зайти на страницу Статьи'
        )
        time.sleep(2)

    def test_can_update_article(self) -> None:
        """тестирует можно ли редактировать Статью"""

        # Гал хочет отредактировать свою Статью
        # Так как она у него уже есть,
        # то он сразу переходит на страницу Статьи
        article_page, guide, user, article = create_user_guide_article_then_go_to_article_page(
            self.browser, self.live_server_url
        )

        # Гал видит кнопку выпадающего меню
        self.assertTrue(
            article_page.article_menu_btn.is_displayed(),
            'Не отображается кнопка меню Статьи'
        )

        # Он ее нажимает
        article_page.article_menu_btn.click()

        # Вниз выпадает меню
        self.assertTrue(
            article_page.article_menu.is_displayed(),
            'Не отображается выпадающее меню Руководства'
        )

        # Гал находит там кнопку редактировать
        self.assertTrue(
            article_page.edit_article_btn.is_displayed(),
            'Не отображается кнопка редактирования'
        )

        # Нажимает ее
        article_page.edit_article_btn.click()

        # И попадает на страницу редактирования Статьи
        edit_article_page = EditArticlePage(self.browser, self.live_server_url, guide.pk, article.pk)

        # Тут он видит поля Назавания и Текст,
        # в которых есть данные, внесенные при создании Статьи
        self.assertTrue(
            edit_article_page.article_name_field.is_displayed(),
            'Поле Названия не отображается'
        )
        self.assertTrue(
            edit_article_page.text_field.is_displayed(),
            'Поле Текста не отображается'
        )

        # Гал пробует обновить данные поля Назавания и Текста
        edit_article_page.article_name_field.send_keys('Обновленное ' + TEST_ARTICLE_NAME)
        edit_article_page.text_field.send_keys('Обновленный текст ' + TEST_ARTICLE_TEXT)

        # Находит кнопку "Сохранить"
        self.assertTrue(
            edit_article_page.save_article_btn.is_displayed(),
            'Кнопка Сохранить не отображается'
        )

        # Нажимает её
        edit_article_page.save_article_btn.click()

        # Гала возвращает на страницу просмотра Статьи
        self.assertIn(
            'Обновленное ' + TEST_ARTICLE_NAME,
            article_page.page_title,
            'Невозможно зайти на страницу Руководства'
        )

    def test_can_open_article(self) -> None:
        """тестирует можно ли открыть страницу Статьи"""

        # У Гала есть Руководсто
        # Гал заходит на страницу Руководства
        guides_page, guide, user = create_user_guide_and_go_to_guide_page(
            self.browser, self.live_server_url
        )
        # Также у него уже есть созданная Статья
        article = create_article(author=user, guide=guide)
        # Он обновляет страницу
        self.browser.refresh()

        # Видит там созданную им Статью
        article_btn = guides_page.get_article(article.pk)

        # Нажимает на нее
        article_btn.click()

        # Его перемещает на страницу Статьи
        article_page = DetailArticlePage(self.browser, self.live_server_url, guide.pk, article.pk)
        self.assertIn(
            TEST_ARTICLE_NAME,
            article_page.page_title
        )

    def test_can_create_new_article(self) -> None:
        """тест можно создать новую статью"""

        # Гал заходит на страницу своего руководства
        guide_page, guide, _ = create_user_guide_and_go_to_guide_page(self.browser, self.live_server_url)

        # Нажимает кнопку добавить Статью
        guide_page.new_article_btn.click()

        # Попадает на страницу добавления Статьи
        new_article_page = NewArticlePage(self.browser, self.live_server_url, guide.pk)
        self.assertIn(
            'Новая статья',
            new_article_page.page_title,
            'Не переходит на страницу создания новой Статьи'
        )

        # Где он может ввести название статьи
        self.assertTrue(new_article_page.article_name_field.is_displayed())
        new_article_page.article_name_field.send_keys(TEST_ARTICLE_NAME)

        # Может сделать запись в текстовое поле
        self.assertTrue(new_article_page.text_field.is_displayed())
        new_article_page.text_field.send_keys(TEST_ARTICLE_TEXT)

        # Находит кнопку сохранить
        self.assertTrue(new_article_page.create_article_btn.is_displayed())

        # Нажимает ее
        new_article_page.create_article_btn.click()

        # Гал попадает на страницу текущего Руководства
        self.assertIn(
            guide.name,
            guide_page.page_title,
            'Не перешло на страницу текущего Руководства'
        )

        # Где он видит созданную им статью
        self.assertTrue(guide_page.is_text_present(TEST_ARTICLE_NAME))
        self.assertTrue(guide_page.is_text_present(TEST_ARTICLE_TEXT))

        # Гал рад, что все получилось
