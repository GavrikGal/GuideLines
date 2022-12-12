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
