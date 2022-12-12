from django.db.models.query import QuerySet
from django.test import TestCase

from ..views import HomePageView
from .utils.services import create_default_guide


class HomePageViewTest(TestCase):
    """Тестирования вьюхи главной страницы"""

    def test_guides_is_in_context_data(self) -> None:
        """Тестирует есть ли в context_data главной страницы Руководства Guides"""
        view = HomePageView()

        self.assertIn(
            'guides',
            view.get_context_data()
        )

    def test_guides_in_context_data_is_set(self) -> None:
        """Тестирует есть ли в context_data главной страницы Руководства Guides"""
        view = HomePageView()

        self.assertIsInstance(
            view.get_context_data()['guides'],
            QuerySet
        )

    def test_guides_in_context_data_is_present(self) -> None:
        """Тестирует чтоб ключ guides в context_data возвращал не пустой Set"""
        view = HomePageView()
        create_default_guide()

        self.assertIsNot(
            0,
            len(view.get_context_data()['guides'])
        )
