from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import Mock, patch

from ..views import UpdateGuideView, DeleteGuideView
from ..models import CustomUser, Guide, Article
from .utils.const import TEST_USERNAME


class DeleteGuideViewTest(TestCase):
    """Тестирует вьюху удаления Руководства"""

    def test_can_not_delete_guide_it_has_any_article(self):
        """Тестирует: нельзя удалить Руководство, если в нем есть хотя бы одна Статья"""
        author = CustomUser.objects.create()
        guide = Guide.objects.create(author=author)
        Article.objects.create(guide=guide, author=author)

        self.client.post(reverse_lazy('guides:delete_guide', kwargs={'guide_pk': guide.pk}))
        self.assertNotEqual(
            len(Guide.objects.all()),
            0,
            'Руководство было удалено из БД'
        )

    def test_user_passes_test_func_passed(self) -> None:
        """Функция test_func миксина UserPassesTestMixin разрешает доступ к вьюхе"""

        author = Mock()
        mock_guide = Mock()
        mock_guide.author = author
        mock_request = Mock()
        mock_request.user = author

        view = DeleteGuideView()
        view.get_object = Mock(return_value=mock_guide)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        author = Mock()
        user = Mock()
        mock_guide = Mock()
        mock_guide.author = author
        mock_request = Mock()
        mock_request.user = user

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

        author = CustomUser.objects.create()
        guide = Guide.objects.create(author=author)
        self.client.post(reverse_lazy('guides:delete_guide', kwargs={'guide_pk': guide.pk}))
        self.assertNotEqual(
            len(Guide.objects.all()),
            0,
            'Руководство удалено из БД'
        )

    def test_no_author_can_not_delete_guide(self):
        """Тестирует может ли не автор удалять своё Руководство"""

        author = CustomUser.objects.create()
        guide = Guide.objects.create(author=author)
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

        author = CustomUser.objects.create()
        guide = Guide.objects.create(author=author)

        self.client.force_login(author)
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

        author = CustomUser(username=TEST_USERNAME)
        mock_guide = Mock()
        mock_guide.author = author
        mock_request = Mock()
        mock_request.user = author

        view = UpdateGuideView()
        view.get_object = Mock(return_value=mock_guide)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        author = CustomUser(username=TEST_USERNAME)
        user = CustomUser(username='Another_test_user')
        mock_guide = Mock()
        mock_guide.author = author
        mock_request = Mock()
        mock_request.user = user

        view = UpdateGuideView()
        view.get_object = Mock(return_value=mock_guide)
        view.request = mock_request

        self.assertFalse(
            view.test_func()
        )



