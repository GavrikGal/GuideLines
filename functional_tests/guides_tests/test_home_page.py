from functional_tests.base import FunctionalTest
from functional_tests.pages.home_page import HomePage



class HomePageTest(FunctionalTest):
    """тест главной страницы"""

    def test_guides_are_present_on_home_page(self) -> None:
        """Тест. Созданное руководство видно на главной странице"""

        # Гал зареганный пользователь, который создал Руководство

        # Он переходит на главную страницу Системы

        # И видит обложку своего Руководства


    def test_layout_and_CSS_styling(self) -> None:
        """тест макета и стилевого оформления"""

        # Гал заходит на главную страницу
        home_page = HomePage(self.browser, self.live_server_url)
        home_page.go_to_page()
        self.browser.set_window_size(1024, 768)

        # И видит, что хеадер страницы находится по центру экрана
        header = home_page.header
        self.assertAlmostEqual(
            header.location['x'] + header.size['width'] / 2,
            512,
            delta=10
        )

    def test_can_open_home_page(self) -> None:
        """тест можно открыть главную страницу"""
        # Гал хочет открыть главную страницу системы.
        # Он вводит адрес
        self.browser.get(self.live_server_url)

        # и спокойно попадает на главную страницу
        # и видит слово GuideLines в тайтле страницы
        self.assertIn(
            'GuideLines',
            self.browser.title
        )

        # Это ли не счастье?
