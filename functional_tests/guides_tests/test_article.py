from unittest import skip

from functional_tests.base import FunctionalTest


class ArticleTest(FunctionalTest):
    """тесты Статей"""

    @skip
    def test_can_create_new_article(self) -> None:
        """тест можно создать новую статью"""

        self.fail("Доделать")
