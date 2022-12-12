from os.path import exists
from os.path import splitext
from shutil import rmtree
from unittest.mock import Mock, patch

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import signals
from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse_lazy

import guides.models
from .views import HomePageView, UpdateArticleView, DeleteArticleView, UpdateGuideView, DeleteGuideView
from .models import CustomUser, Guide, Article


TEST_USERNAME = 'username_gal_test'
TEST_PASSWORD = 'Password12345'
TEST_FIRST_NAME = 'Дмитрий'
TEST_LAST_NAME = 'Гал'
TEST_AVATAR_IMG_NAME = 'gal-avatar-12345.jpg'

TEST_GUIDE_NAME = 'Моё первое тестовое руководство'
TEST_GUIDE_DESCRIPTION = 'Моё описание к первому тестовому руководству. Должно быть много букф, но ' \
                         'надо немного сократиться. Пока. Это было круто'
TEST_GUIDE_COVER_IMG_NAME = 'gal-guide-cover-12345.jpg'
TEST_ARTICLE_NAME = 'Моя первая тестовая статья'


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


class DeleteArticleViewTest(TestCase):
    """Тестирует вьюху удаления Статьи"""

    def test_user_passes_test_func_passed(self) -> None:
        """Функция test_func миксина UserPassesTestMixin разрешает доступ к вьюхе"""

        author = Mock()
        mock_article = Mock()
        mock_article.author = author
        mock_request = Mock()
        mock_request.user = author

        view = DeleteArticleView()
        view.get_object = Mock(return_value=mock_article)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        author = Mock()
        user = Mock()
        mock_article = Mock()
        mock_article.author = author
        mock_request = Mock()
        mock_request.user = user

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

        author = CustomUser.objects.create()
        guide = Guide.objects.create(author=author)
        article = Article.objects.create(guide=guide, author=author)

        self.client.post(reverse_lazy('guides:delete_article', kwargs={'guide_pk': guide.pk,
                                                                       'pk': article.pk}))
        self.assertNotEqual(
            len(Article.objects.all()),
            0,
            'Статья была удалена из БД'
        )

    def test_no_author_can_not_delete_article(self):
        """Тестирует может ли не автор удалять свою Статью"""

        author = CustomUser.objects.create()
        guide = Guide.objects.create(author=author)
        article = Article.objects.create(guide=guide, author=author)
        shaitan = CustomUser.objects.create(username='Shaitan')

        self.client.force_login(shaitan)
        self.client.post(reverse_lazy('guides:delete_article', kwargs={'guide_pk': guide.pk,
                                                                       'pk': article.pk}))
        self.assertNotEqual(
            len(Article.objects.all()),
            0,
            'Статья была удалена из БД'
        )

    def test_author_can_delete_article(self):
        """Тестирует может ли автор удалять свою Статью"""

        author = CustomUser.objects.create()
        guide = Guide.objects.create(author=author)
        article = Article.objects.create(guide=guide, author=author)

        self.client.force_login(author)
        self.client.post(reverse_lazy('guides:delete_article', kwargs={'guide_pk': guide.pk,
                                                                       'pk': article.pk}))
        self.assertEqual(
            len(Article.objects.all()),
            0,
            'Статья НЕ была удалена из БД'
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

        author = CustomUser(username=TEST_USERNAME)
        mock_article = Mock()
        mock_article.author = author
        mock_request = Mock()
        mock_request.user = author

        view = UpdateArticleView()
        view.get_object = Mock(return_value=mock_article)
        view.request = mock_request

        self.assertTrue(
            view.test_func()
        )

    def test_user_passes_test_mixin_test_func_denied(self) -> None:
        """Функция test_func миксина UserPassesTestMixin НЕ разрешает доступ к вьюхе"""

        author = CustomUser(username=TEST_USERNAME)
        user = CustomUser(username='Another_test_user')
        mock_article = Mock()
        mock_article.author = author
        mock_request = Mock()
        mock_request.user = user

        view = UpdateArticleView()
        view.get_object = Mock(return_value=mock_article)
        view.request = mock_request

        self.assertFalse(
            view.test_func()
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


class ArticleViewTest(TestCase):
    """Тестирование вьюхи Статьи"""

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
        Guide.objects.create(name=TEST_GUIDE_NAME,
                             author=CustomUser.objects.create(username=TEST_USERNAME))

        self.assertIsNot(
            0,
            len(view.get_context_data()['guides'])
        )


class CustomUserModelTest(TestCase):
    """Модульное тестирование модели пользователя"""

    def test_custom_user_avatar_upload_path(self) -> None:
        """тест пути загрузки аватарки пользователя"""

        user = CustomUser(username=TEST_USERNAME)
        upload_path = user.get_upload_path(TEST_AVATAR_IMG_NAME)

        self.assertIn(
            user.username + '/' + splitext(TEST_AVATAR_IMG_NAME)[0],
            upload_path
        )

    def test_media_is_upload(self) -> None:
        """тест загружаются ли медиаданные указанные в ImageField модели
        в место хранинения media"""

        user = CustomUser(username=TEST_USERNAME)
        user.avatar = SimpleUploadedFile(TEST_AVATAR_IMG_NAME, b'', content_type='image/jpeg')
        user.save()

        upload_path = user.avatar.name
        absolut_upload_path = settings.MEDIA_ROOT / upload_path

        self.assertTrue(
            exists(absolut_upload_path)
        )

        if exists(settings.MEDIA_ROOT / TEST_USERNAME):
            rmtree(settings.MEDIA_ROOT / TEST_USERNAME, ignore_errors=True)

    def test_delete_user_root_dir_calling(self) -> None:
        """тест: функция удаления корневой медиа-директрории пользователя
        delete_user_root_dir зарегистирована в с сигланах pre_delete моделей джанго"""

        registered_functions = [r[1]() for r in signals.pre_delete.receivers]
        self.assertIn(
            guides.models.delete_user_root_dir,
            registered_functions
        )


class GuideModelTest(TestCase):
    """Модульное тестирование модели Руководства"""

    def test_guide_cover_upload_path(self) -> None:
        """тест пути загрузки обложки Руководства"""

        user = CustomUser(username=TEST_USERNAME)
        guide = Guide(author=user)
        upload_path = guide.get_upload_path(TEST_GUIDE_COVER_IMG_NAME)

        self.assertIn(
            user.username + '/' + splitext(TEST_GUIDE_COVER_IMG_NAME)[0],
            upload_path
        )


class ReadyUnitTest(TestCase):
    """Модульное тестирование"""

    def test_can_start_test(self) -> None:
        """тесты могут запускаться"""
        self.assertEqual(1 + 2, 3)
