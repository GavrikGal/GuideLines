import time
from unittest import skip

from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.pages.detail_guide_page import DetailGuidePage
from functional_tests.pages.new_article_page import NewArticlePage
from functional_tests.const import (TEST_ARTICLE_NAME, TEST_ARTICLE_TEXT)


class ArticleTest(FunctionalTest):
    """тесты Статей"""

    def test_can_create_new_article(self) -> None:
        """тест можно создать новую статью"""

        # Гал заходит на страницу своего руководства
        user = self.create_user_and_pre_authenticated_session()
        guide = self.create_guide(user)
        detail_guide_page = DetailGuidePage(self, guide.pk)
        detail_guide_page.go_to_page()

        # Нажимает кнопку добавить Статью
        detail_guide_page.new_article_btn.click()

        # Попадает на страницу добавления Статьи
        new_article_page = NewArticlePage(self, guide.pk)
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
            detail_guide_page.page_title,
            'Не перешло на страницу текущего Руководства'
        )

        # Где он видит созданную им статью
        self.assertTrue(detail_guide_page.find_text(TEST_ARTICLE_NAME))
        self.assertTrue(detail_guide_page.find_text(TEST_ARTICLE_TEXT))

        print('_______Меняю master___________')
        print('Тут была экспериментальная ветка 1')
        print('Мне понадобилось переключиться на еще одну экспериментальную ветку №2')

        print('Новая ветка 2')
        print('Работаем работу')
        print('Все сделали в ветке-2')
        print('Пробуем смерджить с мастером и вернуться к ветке-1')

        # Гал рад, что все получилось
