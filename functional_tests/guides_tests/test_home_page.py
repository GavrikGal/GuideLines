from os.path import splitext, basename

from functional_tests.base import FunctionalTest
from functional_tests.pages.home_page import HomePage
from functional_tests.const import (
    TEST_LAST_NAME, TEST_GUIDE_NAME, TEST_FIRST_NAME,
    TEST_GUIDE_DESCRIPTION, TEST_GUIDE_COVER_IMG_PATH
)
from functional_tests.utils.services import create_user_guide_and_go_to_guide_page


class HomePageTest(FunctionalTest):
    """тест главной страницы"""

    def test_guide_can_be_opened(self) -> None:
        """Тестирует можно ли перейти на страницу Руководства с главной"""

        # Гал зарезанный пользователь, имеющий своё Руководство
        guide_page, guide, _ = create_user_guide_and_go_to_guide_page(self.browser, self.live_server_url)

        # Он заходит на главную
        home_page = HomePage(self.browser, self.live_server_url)
        home_page.go_to_page()

        # Нажимает на своё руководство
        guide_btn = home_page.get_guide(guide.pk)
        guide_btn.click()

        # И его переносит на страницу Руководства
        self.assertIn(
            guide.name,
            guide_page.page_title,
            'Не перешло на страницу руководства'
        )

    def test_guides_are_present(self) -> None:
        """Тест. Созданное руководство видно на главной странице"""

        # Гал зареганный пользователь, который создал Руководство
        _, guide, _ = create_user_guide_and_go_to_guide_page(self.browser, self.live_server_url)

        # Он переходит на главную страницу Системы
        home_page = HomePage(self.browser, self.live_server_url)
        home_page.go_to_page()

        # И там видит название своего Руководства
        self.assertTrue(
            home_page.is_text_present(TEST_GUIDE_NAME),
            'Нет названия Руководства'
        )

        # Описание Руководства
        self.assertTrue(
            home_page.is_text_present(TEST_GUIDE_DESCRIPTION),
            'Нет описания Руководства'
        )

        # То, что он автор руководства
        self.assertIn(
            TEST_FIRST_NAME,
            home_page.get_guide_author(guide.pk),
            'Нет имени автора Руководства'
        )
        self.assertIn(
            TEST_LAST_NAME,
            home_page.get_guide_author(guide.pk),
            'Нет фамилии автора Руководства'
        )

        # И видит картинку обложки своего Руководства
        cover_img = home_page.get_guide_cover_img(guide.pk)
        self.assertTrue(
            cover_img.is_displayed(),
            'Картинка обложки Руководства не отображается'
        )
        self.assertIn(
            splitext(basename(TEST_GUIDE_COVER_IMG_PATH))[0],
            cover_img.get_attribute('src'),
            'Не та картинка Руководства'
        )

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
