from functional_tests.base import FunctionalTest
from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.buttons import BaseButton


class HomePage(BasePage):
    """Домашняя страница"""

    def __init__(self, test: FunctionalTest) -> None:
        super().__init__(test, '/')  # установка адреса страницы
        self.new_guide_btn = BaseButton(test, id_="id_add_guide_btn")

