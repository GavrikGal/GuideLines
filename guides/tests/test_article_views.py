from django.test import TestCase
from django.urls import reverse_lazy
from unittest.mock import Mock, patch

from ..views import UpdateArticleView, DeleteArticleView, DetailArticleView, publish_article
from ..models import CustomUser, Article
from .utils.services import create_default_article


class PublishArticleTest(TestCase):
    """Тестирует вьюху публикации Статьи"""

    def test_publish_article_make_article_not_draft(self) -> None:
        """Тестирует, вьюха publish_article делает Статью не черновиком"""
        article = create_default_article()
        publish_article(Mock(), article.guide.pk, article.pk)
        self.assertFalse(
            Article.objects.get(pk=article.pk).draft,
            'Статья всё ещё черновик'
        )


class DetailArticleViewTest(TestCase):
    """Тестирует вьюху Статьи"""

    def test_mixins_test_func_allow_access_if_article_is_draft_and_user_is_author(self):
        """Функция test_func миксина UserPassesTestMixin возвращает True для Черновика, если пользователь автор"""

        mock_article = Mock()
        mock_article.draft = True
        mock_request = Mock()
        mock_request.user = mock_article.author  # Пользователь - это автор

        view = DetailArticleView()
        view.request = mock_request
        view.get_object = Mock(return_value=mock_article)

        self.assertTrue(
            view.test_func()
        )

    def test_mixins_test_func_deny_access_if_article_is_draft_and_user_is_not_author(self):
        """Функция test_func миксина UserPassesTestMixin возвращает False для Черновика, если пользователь не автор"""

        mock_article = Mock()
        mock_article.draft = True
        mock_request = Mock()

        view = DetailArticleView()
        view.request = mock_request
        view.get_object = Mock(return_value=mock_article)

        self.assertFalse(
            view.test_func()
        )

    def test_mixins_test_func_deny_access_if_article_is_draft_and_anonymous(self):
        """Функция test_func миксина UserPassesTestMixin возвращает False для Черновика и анонима"""

        mock_article = Mock()
        mock_article.draft = True
        mock_request = Mock()

        view = DetailArticleView()
        view.request = mock_request
        view.request.user.is_authenticated = False
        view.get_object = Mock(return_value=mock_article)

        self.assertFalse(
            view.test_func()
        )

    def test_mixins_test_func_allow_access_if_not_draft(self):
        """Функция test_func миксина UserPassesTestMixin возвращает True если статья не Черновик"""

        mock_article = Mock()
        mock_article.draft = False

        view = DetailArticleView()
        view.get_object = Mock(return_value=mock_article)

        self.assertTrue(
            view.test_func()
        )

    @patch('guides.views.DetailArticleView.test_func', return_value=True)
    def test_mixins_test_func_called(self, mock_test_func) -> None:
        """Функция test_func миксина UserPassesTestMixin вызывается"""

        self.client.post(reverse_lazy('guides:detail_article', kwargs={'guide_pk': 1,
                                                                       'pk': 1}))
        self.assertTrue(
            mock_test_func.called
        )


class DeleteArticleViewTest(TestCase):
    """Тестирует вьюху удаления Статьи"""

    def test_user_passes_test_func_passed(self) -> None:
        """Функция test_func миксина UserPassesTestMixin разрешает доступ к вьюхе"""

        mock_article = Mock()
        mock_request = Mock()

        mock_request.user = mock_article.author     # Пользователь - это автор

        view = DeleteArticleView()
        view.get_object = Mock(return_value=mock_article)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        mock_article = Mock()
        mock_request = Mock()

        view = DeleteArticleView()
        view.get_object = Mock(return_value=mock_article)
        view.request = mock_request

        self.assertFalse(
            view.test_func()
        )

    @patch('guides.views.DeleteArticleView.test_func', return_value=True)
    def test_user_passes_test_mixin_func_called(self, mock_test_func) -> None:
        """Функция test_func миксина UserPassesTestMixin вызывается"""

        author = CustomUser.objects.create()
        self.client.force_login(author)
        self.client.post(reverse_lazy('guides:delete_article', kwargs={'guide_pk': 1,
                                                                       'pk': 1}))

        self.assertTrue(
            mock_test_func.called
        )

    def test_only_authenticated_author_can_delete_article(self):
        """Тестирует может ли не автор удалять свою Статью"""

        article = create_default_article()

        self.client.post(reverse_lazy('guides:delete_article', kwargs={'guide_pk': article.guide.pk,
                                                                       'pk': article.pk}))
        self.assertNotEqual(
            len(Article.objects.all()),
            0,
            'Статья была удалена из БД'
        )

    def test_no_author_can_not_delete_article(self):
        """Тестирует может ли не автор удалять свою Статью"""

        article = create_default_article()
        shaitan = CustomUser.objects.create(username='Shaitan')

        self.client.force_login(shaitan)
        self.client.post(reverse_lazy('guides:delete_article', kwargs={'guide_pk': article.guide.pk,
                                                                       'pk': article.pk}))
        self.assertNotEqual(
            len(Article.objects.all()),
            0,
            'Статья была удалена из БД'
        )

    def test_author_can_delete_article(self):
        """Тестирует может ли автор удалять свою Статью"""

        article = create_default_article()

        self.client.force_login(article.author)
        self.client.post(reverse_lazy('guides:delete_article', kwargs={'guide_pk': article.guide.pk,
                                                                       'pk': article.pk}))
        self.assertEqual(
            len(Article.objects.all()),
            0,
            'Статья НЕ была удалена из БД'
        )

    def test_delete_success_url(self) -> None:
        """Тестирует правильно ли формируется success_url методом get_success_url"""

        test_guide_pk = 1

        mock_article = Mock()
        mock_article.guide.pk = test_guide_pk

        view = DeleteArticleView()
        view.object = mock_article

        self.assertEqual(
            reverse_lazy('guides:detail_guide', kwargs={'guide_pk': test_guide_pk}),
            view.get_success_url()
        )


class UpdateArticleViewTest(TestCase):
    """Тестирует вьюху обновления Статьи"""

    @patch('guides.views.UpdateArticleView.test_func', return_value=True)
    def test_user_passes_test_mixin_func_called(self, mock_test_func) -> None:
        """Функция test_func миксина UserPassesTestMixin вызывается"""

        author = CustomUser.objects.create()
        self.client.force_login(author)
        self.client.get(reverse_lazy('guides:edit_article', kwargs={'guide_pk': 1,
                                                                    'pk': 1}))

        self.assertTrue(
            mock_test_func.called
        )

    def test_user_passes_test_func_passed(self) -> None:
        """Функция test_func миксина UserPassesTestMixin разрешает доступ к вьюхе"""

        mock_article = Mock()
        mock_request = Mock()
        mock_request.user = mock_article.author     # Пользователь - это автор

        view = UpdateArticleView()
        view.get_object = Mock(return_value=mock_article)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        mock_article = Mock()
        mock_request = Mock()

        view = UpdateArticleView()
        view.get_object = Mock(return_value=mock_article)
        view.request = mock_request

        self.assertFalse(
            view.test_func()
        )

    def test_update_success_url(self) -> None:
        """Тестирует правильно ли формируется success_url методом get_success_url"""

        test_guide_pk = 1
        test_article_pk = 1

        mock_article = Mock()
        mock_article.pk = test_article_pk
        mock_article.guide.pk = test_guide_pk

        view = UpdateArticleView()
        view.object = mock_article

        self.assertEqual(
            reverse_lazy('guides:detail_article', kwargs={'guide_pk': test_guide_pk, 'pk': test_article_pk}),
            view.get_success_url()
        )
