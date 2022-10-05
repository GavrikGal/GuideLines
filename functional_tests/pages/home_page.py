from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage


class HomePage(BasePage):
    """Домашняя страница"""

    def __init__(self, test: FunctionalTest) -> None:
        super().__init__(test, '/')  # установка адреса страницы

