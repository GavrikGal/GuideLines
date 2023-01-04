from unittest.mock import Mock

from .const import TEST_USERNAME

from ...models import CustomUser, Guide, Article
from ...views import DetailArticleView


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


def create_detail_article_view_with_mock_request_and_article(
        article_is_draft: bool = True,
        user_is_article_author: bool = False) -> DetailArticleView:
    """
    Создает вьюху DetailArticleView, где в request установлен Mock-объект, а get_object вернет Mock-объект
    :param user_is_article_author: автор Статьи - это тестовый пользователь
    :param article_is_draft: Статья - это черновик
    :return: вьюха DetailArticleView, где в request установлен Mock-объект
    """
    view = DetailArticleView()
    view.request = Mock()

    mock_article = Mock()
    mock_article.draft = article_is_draft
    view.get_object = Mock(return_value=mock_article)

    if user_is_article_author:
        view.request.user = mock_article.author     # Пользователь - это автор

    return view
