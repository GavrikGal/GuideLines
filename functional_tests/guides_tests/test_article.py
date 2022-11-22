from functional_tests.base import FunctionalTest
from functional_tests.pages.new_article_page import NewArticlePage
from functional_tests.pages.detail_article_page import DetailArticlePage
from functional_tests.const import (TEST_ARTICLE_NAME, TEST_ARTICLE_TEXT)
from functional_tests.utils.services import create_user_guide_and_go_to_guide_page

from guides.models import Article


class ArticleTest(FunctionalTest):
    """тесты Статей"""

    def test_can_open_article(self) -> None:
        """тестирует можно ли открыть страницу Статьи"""

        # У Гала есть Руководсто
        guides_page, guide, user = create_user_guide_and_go_to_guide_page(self.browser, self.live_server_url)

        # Также у него уже есть созданная Статья
        article = Article.objects.create(name=TEST_ARTICLE_NAME,
                                         text=TEST_ARTICLE_TEXT,
                                         author=user,
                                         guide=guide)

        # Гал заходит на страницу Руководства
        guides_page.go_to_page()

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
