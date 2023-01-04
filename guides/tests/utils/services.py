from unittest.mock import Mock

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import View
from typing import Union

from django.views.generic.edit import FormMixin

from .const import TEST_USERNAME

from ...models import CustomUser, Guide, Article


def create_default_article() -> Article:
    """
    Создаёт стандартных автора CustomUser, Руководство Guide и Статью Article
    :return: Статью Article с корректнтым автором и Руководством
    """
    author = CustomUser.objects.create(username=TEST_USERNAME)
    guide = Guide.objects.create(author=author)
    article = Article.objects.create(guide=guide, author=author)
    return article


def create_default_guide() -> Guide:
    """
    Создаёт стандартных автора CustomUser и Руководство Guide
    :return: Руководство Guide с корретным автором
    """
    author = CustomUser.objects.create(username=TEST_USERNAME)
    guide = Guide.objects.create(author=author)
    return guide


def add_mock_request_and_mock_article_to_view(
        view: View,
        article_is_draft: bool = True,
        user_is_article_author: bool = False,
        article_pk: int = 1,
        guide_pk: int = 1) -> Union[View, UserPassesTestMixin, FormMixin]:
    """
    Добавляет во вьюху вместо view.request Mock-объект, а view.get_object() вернет Mock-объект похожий на Article
    :param article_pk: pk от Статьи
    :param guide_pk: pk от Руководства, которому принадлежит Статья
    :param view: Вьюха, куда надо добавить mock-объекты
    :param user_is_article_author: автор Статьи - это тестовый пользователь
    :param article_is_draft: Статья - это черновик
    :return: вьюха DetailArticleView, где в request установлен Mock-объект
    """

    mock_article = Mock()
    mock_article.draft = article_is_draft
    mock_article.pk = article_pk
    mock_article.guide.pk = guide_pk
    view.object = mock_article
    view.get_object = Mock(return_value=mock_article)

    view.request = Mock()

    if user_is_article_author:
        view.request.user = mock_article.author     # Пользователь - это автор

    return view
