from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import Mock, patch

from ..views import UpdateGuideView, DeleteGuideView, DetailGuideView
from ..models import CustomUser, Guide
from .utils.services import create_default_article, create_default_guide


class DetailGuideViewTest(TestCase):
    """Тесты вьюхи DetailGuideView"""

    def test_articles_in_context_data_without_drafts_for_no_author(self) -> None:
        """Тестирует, чтобы Статьи в context_data были без черновиков для обычного пользователя (не автора)"""
        article1 = create_default_article()
        guide = article.guide
        view = DetailGuideView()
        view.object = guide

    def test_articles_in_context_data_is_present(self) -> None:
        """Тестирует чтоб ключ articles в context_data возвращал не пустой Set"""
        article = create_default_article()
        guide = article.guide
        view = DetailGuideView()
        view.object = guide

        self.assertIsNot(
            0,
            len(view.get_context_data()['articles'])
        )

    def test_articles_in_context_data_is_set(self) -> None:
        """Тестирует, что Статьи articles в context_data - это QuerySet"""
        guide = create_default_guide()
        view = DetailGuideView()
        view.object = guide

        self.assertIsInstance(
            view.get_context_data()['articles'],
            QuerySet
        )

    def test_articles_is_in_context_data(self) -> None:
        """Тестирует есть ли в контексте context_data ключ Статей articles"""
        guide = create_default_guide()
        view = DetailGuideView()
        view.object = guide

        self.assertIn(
            'articles',
            view.get_context_data()
        )

    @patch('guides.views.DetailGuideView.get_context_data', return_value=None)
    def test_get_context_data_called(self, mock_get_context_data: Mock) -> None:
        """Функция get_context_data вьюхи DetailGuideView вызывается"""

        guide = create_default_guide()
        self.client.get(reverse_lazy('guides:detail_guide', kwargs={'guide_pk': guide.pk}))

        self.assertTrue(
            mock_get_context_data.called
        )

class DeleteGuideViewTest(TestCase):
    """Тестирует вьюху удаления Руководства"""

    def test_can_not_delete_guide_it_has_any_article(self):
        """Тестирует: нельзя удалить Руководство, если в нем есть хотя бы одна Статья"""

        article = create_default_article()

        self.client.post(reverse_lazy('guides:delete_guide', kwargs={'guide_pk': article.guide.pk}))
        self.assertNotEqual(
            len(Guide.objects.all()),
            0,
            'Руководство было удалено из БД'
        )

    def test_user_passes_test_func_passed(self) -> None:
        """Функция test_func миксина UserPassesTestMixin разрешает доступ к вьюхе"""

        mock_guide = Mock()
        mock_request = Mock()
        mock_request.user = mock_guide.author       # Пользователь - это автор

        view = DeleteGuideView()
        view.get_object = Mock(return_value=mock_guide)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        mock_guide = Mock()
        mock_request = Mock()

        view = DeleteGuideView()
        view.get_object = Mock(return_value=mock_guide)
        view.request = mock_request

        self.assertFalse(
            view.test_func()
        )

    @patch('guides.views.DeleteGuideView.test_func', return_value=True)
    def test_user_passes_test_mixin_func_called(self, mock_test_func) -> None:
        """Функция test_func миксина UserPassesTestMixin вызывается"""

        author = CustomUser.objects.create()
        self.client.force_login(author)
        self.client.post(reverse_lazy('guides:delete_guide', kwargs={'guide_pk': 1}))

        self.assertTrue(
            mock_test_func.called
        )

    def test_only_authenticated_author_can_delete_guide(self):
        """Тестирует может ли не автор удалять своё Руководство"""

        guide = create_default_guide()
        self.client.post(reverse_lazy('guides:delete_guide', kwargs={'guide_pk': guide.pk}))
        self.assertNotEqual(
            len(Guide.objects.all()),
            0,
            'Руководство удалено из БД'
        )

    def test_no_author_can_not_delete_guide(self):
        """Тестирует может ли не автор удалять своё Руководство"""

        guide = create_default_guide()
        shaitan = CustomUser.objects.create(username='Shaitan')

        self.client.force_login(shaitan)
        self.client.post(reverse_lazy('guides:delete_guide', kwargs={'guide_pk': guide.pk}))
        self.assertNotEqual(
            len(Guide.objects.all()),
            0,
            'Руководство удалено из БД'
        )

    def test_author_can_delete_guide(self):
        """Тестирует может ли автор удалять своё Руководство"""

        guide = create_default_guide()

        self.client.force_login(guide.author)
        self.client.post(reverse_lazy('guides:delete_guide', kwargs={'guide_pk': guide.pk}))
        self.assertEqual(
            len(Guide.objects.all()),
            0,
            'Руководство НЕ удалено из БД'
        )


class UpdateGuideViewTest(TestCase):
    """Тестирует вьюху обновления Руководства"""

    @patch('guides.views.UpdateGuideView.test_func', return_value=True)
    def test_user_passes_test_mixin_func_called(self, mock_test_func) -> None:
        """Функция test_func миксина UserPassesTestMixin вызывается"""

        author = CustomUser.objects.create()
        self.client.force_login(author)
        self.client.get(reverse_lazy('guides:edit_guide', kwargs={'guide_pk': 1}))

        self.assertTrue(
            mock_test_func.called
        )

    def test_user_passes_test_mixin_test_func_passed(self) -> None:
        """Функция test_func миксина UserPassesTestMixin разрешает доступ к вьюхе"""

        mock_guide = Mock()
        mock_request = Mock()
        mock_request.user = mock_guide.author        # Пользователь - это автор

        view = UpdateGuideView()
        view.get_object = Mock(return_value=mock_guide)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        mock_guide = Mock()
        mock_request = Mock()

        view = UpdateGuideView()
        view.get_object = Mock(return_value=mock_guide)
        view.request = mock_request

        self.assertFalse(
            view.test_func()
        )



