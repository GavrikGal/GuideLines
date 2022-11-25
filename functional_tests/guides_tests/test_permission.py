import time

from functional_tests.base import FunctionalTest
from functional_tests.pages.home_page import HomePage
from functional_tests.pages.new_guide_page import NewGuidePage
from functional_tests.pages.detail_guide_page import DetailGuidePage
from functional_tests.pages.new_article_page import NewArticlePage
from functional_tests.pages.edit_guide_page import EditGuidePage
from functional_tests.utils.services import (
    create_user, create_user_and_pre_authenticated_session, create_guide,
    create_user_guide_and_go_to_guide_page, create_guide_and_user_without_authenticated
)


class GuidesTest(FunctionalTest):
    """тесты прав доступа к Руководствам"""

    def test_must_not_open_edit_guide_page_if_no_author(self) -> None:
        """Тестирует: НЕ должна быть возможность перейти на страницу редактирования Руководства
        пользователю, НЕ являющемуся автором данного Руководства"""

        # Гал создал Руководствао
        guide, _ = create_guide_and_user_without_authenticated()

        # Шайтан просто зареганный пользователь
        create_user_and_pre_authenticated_session(self.browser, self.live_server_url, username='Shaitan')

        # Он пытается перейти на страницу редактирования Руководства
        edit_guide_page = EditGuidePage(self.browser, self.live_server_url, guide.pk)
        edit_guide_page.go_to_page_without_wait()
        # И он НЕ должен туда попасть
        self.assertNotIn(
            'Редактировать',
            edit_guide_page.page_title,
            'Есть возможность перейти на страницу редактирования Руководства'
        )
        self.fail('Доделать')

    def test_can_open_edit_guide_page_if_author(self) -> None:
        """Тестирует: должна быть возможность перейти на страницу редактирования Руководства
        пользователю, являющемуся автором данного Руководства"""

        # Гал идентифицированный в системе пользователь
        _, guide, _ = create_user_guide_and_go_to_guide_page(self.browser, self.live_server_url)

        # Он заходит на страницу редактирования Руководства
        edit_guide_page = EditGuidePage(self.browser, self.live_server_url, guide.pk)
        edit_guide_page.go_to_page_without_wait()

        # И он должен туда попасть
        self.assertIn(
            'Редактировать',
            edit_guide_page.page_title,
            'Не может на страницу редактирования Руководства'
        )

    def test_must_not_see_edit_guide_button_if_no_author(self) -> None:
        """Тестирует: НЕ должна быть видна кнопка редактирования Руководства
        пользователю НЕ являющимуся автором этого Руководства"""

        # Гал пользователь, который написал Руководсто
        guide, _ = create_guide_and_user_without_authenticated()

        # Шайтан просто идентифициированный в системе пользователь
        create_user_and_pre_authenticated_session(self.browser, self.live_server_url, username='Shaitan')

        # Он заходит на страницу Руководства
        guide_page = DetailGuidePage(self.browser, self.live_server_url, guide.pk)
        guide_page.go_to_page()

        # И НЕ видит там кнопки выпадающего меню на Руководстве
        self.assertFalse(
            guide_page.guide_menu_btn.is_displayed(),
            'Видна кнопка выпадающего меню Руководства'
        )

    def test_can_see_edit_guide_button_if_author(self) -> None:
        """Тестирует: должна быть видна кнопка редактирования Руководства
        пользователю являющимуся автором этого Руководства"""

        # Гал пользователь, который написал Руководсто
        # Он заходит на страницу Руководства
        guide_page, guide, user = create_user_guide_and_go_to_guide_page(self.browser, self.live_server_url)

        # И видит там кнопки выпадающего меню на Руководстве
        self.assertTrue(
            guide_page.guide_menu_btn.is_displayed(),
            'Не видна кнопка выпадающего меню Руководства'
        )

    def test_must_not_see_new_guide_button_without_signing_in(self) -> None:
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

    def test_must_not_open_new_guide_page_without_signing_in(self) -> None:
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

    def test_must_not_see_new_article_button_without_signing_in(self) -> None:
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

    def test_must_not_open_new_article_page_without_signing_in(self) -> None:
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
