from unittest import skip

from functional_tests.base import FunctionalTest


class ArticleTest(FunctionalTest):
    """тесты Статей"""

    @skip
    def test_can_create_new_article(self) -> None:
        """тест можно создать новую статью"""

        # Гал заходит на страницу своего руководства

        # Нажимает кнопку добавить Статью

        # Попадает на страницу добавления Статьи

        self.fail("Доделать")
