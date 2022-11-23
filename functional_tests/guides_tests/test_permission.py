from functional_tests.base import FunctionalTest
from functional_tests.pages.home_page import HomePage
from functional_tests.pages.new_guide_page import NewGuidePage
from functional_tests.pages.detail_guide_page import DetailGuidePage
from functional_tests.pages.new_article_page import NewArticlePage
from functional_tests.utils.services import create_user, create_user_and_pre_authenticated_session, create_guide


class GuidesTest(FunctionalTest):
    """тесты прав доступа к Руководствам"""

    def test_can_not_see_new_guide_button_without_signing_in(self) -> None:
        """Тестирует: НЕ должна быть видна кнопка добавления нового Руководства
        пользователю НЕ вошедшему в систему"""

        # Шайтан не идентифицированный в системе пользователь
        create_user()

        # Он заходит на главную страницу
        home_page = HomePage(self.browser, self.live_server_url)
        home_page.go_to_page()

        # И не видит там кнопки добавления нового Руководства
        self.assertFalse(
            home_page.new_guide_btn.is_displayed(),
            'Видна кнопка добавления нового Руководства'
        )

    def test_can_see_new_guide_button_with_signing_in(self) -> None:
        """Тестирует: должна быть видна кнопка добавления нового Руководства
        пользователю вошедшему в систему"""

        # Гал идентифицированный в системе пользователь
        create_user_and_pre_authenticated_session(self.browser, self.live_server_url)

        # Он заходит на главную страницу
        home_page = HomePage(self.browser, self.live_server_url)
        home_page.go_to_page()

        # И видит там кнопки добавления нового Руководства
        self.assertTrue(
            home_page.new_guide_btn.is_displayed(),
            'Не видна кнопка добавления нового Руководства'
        )

    def test_can_not_open_new_guide_page_without_signing_in(self) -> None:
        """Тестирует: НЕ должна быть возможность перейти на страницу добавления нового Руководства
        пользователю НЕ вошедшему в систему"""

        # Шайтан не идентифицированный в системе пользователь
        create_user()

        # Он хочет зайти на страницу добавления нового Руководства
        new_guide_page = NewGuidePage(self.browser, self.live_server_url)
        new_guide_page.go_to_page_without_wait()

        # Он НЕ должен туда попасть
        self.assertNotIn(
            'Новое Руководство',
            new_guide_page.page_title,
            'Есть возможность зайти на страницу Нового Руководства'
        )

    def test_can_open_new_guide_page_with_signing_in(self) -> None:
        """Тестирует: должна быть возможность перейти на страницу добавления нового Руководства
        пользователю вошедшему в систему"""

        # Гал идентифицированный в системе пользователь
        create_user_and_pre_authenticated_session(self.browser, self.live_server_url)

        # Он хочет зайти на страницу добавления нового Руководства
        new_guide_page = NewGuidePage(self.browser, self.live_server_url)
        new_guide_page.go_to_page_without_wait()

        # И он должен туда попасть
        self.assertIn(
            'Новое Руководство',
            new_guide_page.page_title,
            'Не может зайти на страницу Нового Руководства'
        )


class ArticleTest(FunctionalTest):
    """тесты прав доступа к Статьям"""

    def test_can_not_see_new_article_button_without_signing_in(self) -> None:
        """Тестирует: НЕ должна быть видна кнопка добавления новой Статьи
        пользователю НЕ вошедшему в систему"""

        # Шайтан не идентифицированный в системе пользователь (возможно хакер, а может автор)
        user = create_user()

        # В системе есть готовое Руководство
        guide = create_guide(user)

        # Он заходит на страницу Руководства
        guide_page = DetailGuidePage(self.browser, self.live_server_url, guide.pk)
        guide_page.go_to_page()

        # И НЕ видит там кнопки добавления новой Статьи
        self.assertFalse(
            guide_page.new_article_btn.is_displayed(),
            'Видна кнопка добавления новой Статьи'
        )

    def test_can_see_new_article_button_with_signing_in(self) -> None:
        """Тестирует: должна быть видна кнопка добавления новой Статьи
        пользователю вошедшему в систему"""

        # Гал идентифицированный в системе пользователь
        user = create_user_and_pre_authenticated_session(self.browser, self.live_server_url)

        # В системе есть готовое Руководство
        guide = create_guide(user)

        # Он заходит на страницу Руководства
        guide_page = DetailGuidePage(self.browser, self.live_server_url, guide.pk)
        guide_page.go_to_page()

        # И видит там кнопку добавления новой Статьи
        self.assertTrue(
            guide_page.new_article_btn.is_displayed(),
            'Не видна кнопка добавления новой Статьи'
        )

    def test_can_not_open_new_article_page_without_signing_in(self) -> None:
        """Тестирует: НЕ должна быть возможность перейти на страницу добавления новой Статьи
        пользователю НЕ вошедшему в систему"""

        # Шайтан не идентифицированный в системе пользователь (возможно хакер, а может автор)
        user = create_user()

        # В системе есть готовое Руководство
        guide = create_guide(user)

        # Он хочет зайти на страницу добавления новой Статьи
        new_article_page = NewArticlePage(self.browser, self.live_server_url, guide.pk)
        new_article_page.go_to_page_without_wait()

        # Он НЕ должен туда попасть
        self.assertNotIn(
            'Новая статья',
            new_article_page.page_title,
            'Есть возможность зайти на страницу Новой Статьи'
        )

    def test_can_open_new_article_page_with_signing_in(self) -> None:
        """Тестирует: должна быть возможность перейти на страницу добавления новой Статьи
        пользователю вошедшему в систему"""

        # Гал идентифицированный в системе пользователь
        user = create_user_and_pre_authenticated_session(self.browser, self.live_server_url)

        # В системе есть готовое Руководство
        guide = create_guide(user)

        # Он хочет зайти на страницу добавления новой Статьи
        new_article_page = NewArticlePage(self.browser, self.live_server_url, guide.pk)
        new_article_page.go_to_page_without_wait()

        # И он должен туда попасть
        self.assertIn(
            'Новая статья',
            new_article_page.page_title,
            'Не может зайти на страницу Новой Статьи'
        )
