from typing import Optional

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY,
    get_user_model
)

from selenium.webdriver.firefox.webdriver import WebDriver

from functional_tests.utils.const import (
    TEST_GUIDE_DESCRIPTION, TEST_GUIDE_COVER_IMG_PATH, TEST_GUIDE_NAME, TEST_USERNAME, TEST_PASSWORD, TEST_FIRST_NAME,
    TEST_LAST_NAME, TEST_ARTICLE_NAME, TEST_ARTICLE_TEXT,
)
from functional_tests.pages.detail_guide_page import DetailGuidePage
from functional_tests.pages.detail_article_page import DetailArticlePage
from guides.models import Guide, CustomUser, Article


def create_article_and_guide_and_user_without_authenticated() -> tuple[Article, Guide, CustomUser]:
    """
    Создает НЕ залогиненого пользоватея CustomUser, Руководство Guide и Статью Article
    :return: кортеж из Статьи, Руководства и Пользователя
    """
    guide, user = create_guide_and_user_without_authenticated()
    article = create_article(user, guide)
    article.draft = False
    article.save()
    return article, guide, user


def create_guide_and_user_without_authenticated(
        description: Optional[str] = TEST_GUIDE_DESCRIPTION,
        cover_path: Optional[str] = TEST_GUIDE_COVER_IMG_PATH) -> tuple[Guide, CustomUser]:
    """
    Создает НЕ залогиненогого пользователя CustomUser, Руководство Guide
    :param browser: Драйвер вэб-браузера
    :param live_server_url: корневой адрес веб-приложения
    :param description: Добавить описание. Опциональный. По умолчанию const.TEST_GUIDE_DESCRIPTION.
    При None - без описания
    :param cover_path: Путь к обложке Руководства. Опциональный. По умолчанию const.TEST_GUIDE_COVER_IMG_PATH.
    При None - без обложки
    :return: кортеж из Руководства Guide и пользователя CustomUser
    """
    user = create_user()
    guide = create_guide(user, description=description, cover_path=cover_path)
    return guide, user


def create_article(author: CustomUser, guide: Guide, name: str = TEST_ARTICLE_NAME,
                   text: Optional[str] = TEST_ARTICLE_TEXT, draft: bool = True) -> Article:
    """Создает Статью в Руководстве Guide с автором author, названием name и текстом text.
    Если не задавать параметры name, text то будут испозованы тестовые
    значения поумолчанию"""
    article = Article.objects.create(author=author, guide=guide, name=name, text=text, draft=draft)
    return article


def create_user_guide_article_then_go_to_article_page(
        browser: WebDriver,
        live_server_url: str,
        description: Optional[str] = TEST_GUIDE_DESCRIPTION,
        cover_path: Optional[str] = TEST_GUIDE_COVER_IMG_PATH,
        article_is_draft: bool = True) -> tuple[DetailArticlePage, Guide, CustomUser, Article]:
    """
    Создает залогиненогого пользователя CustomUser, Руководство Guide
    и переходит настраницу Руководства.
    :param browser: Драйвер вэб-браузера
    :param live_server_url: корневой адрес веб-приложения
    :param description: Добавить описание. Опциональный. По умолчанию const.TEST_GUIDE_DESCRIPTION.
    При None - без описания
    :param cover_path: Путь к обложке Руководства. Опциональный. По умолчанию const.TEST_GUIDE_COVER_IMG_PATH.
    При None - без обложки
    :return: кортеж из тест-страницы Руководства DetailGuidePage, Руководства Guide, пользователя CustomUser
    """
    user = create_user_and_pre_authenticated_session(browser, live_server_url)
    guide = create_guide(user, description=description, cover_path=cover_path)
    article = create_article(name=TEST_ARTICLE_NAME,
                             text=TEST_ARTICLE_TEXT,
                             author=user,
                             guide=guide,
                             draft=article_is_draft)
    # article = Article.objects.create(name=TEST_ARTICLE_NAME,
    #                                  text=TEST_ARTICLE_TEXT,
    #                                  author=user,
    #                                  guide=guide,
    #                                  draft=article_is_draft)
    article_page = DetailArticlePage(browser, live_server_url, guide.pk, article.pk)
    article_page.go_to_page()
    return article_page, guide, user, article


def create_user_guide_and_go_to_guide_page(
        browser: WebDriver,
        live_server_url: str,
        description: Optional[str] = TEST_GUIDE_DESCRIPTION,
        cover_path: Optional[str] = TEST_GUIDE_COVER_IMG_PATH) -> tuple[DetailGuidePage, Guide, CustomUser]:
    """
    Создает залогиненогого пользователя CustomUser, Руководство Guide
    и переходит настраницу Руководства.
    :param article_is_draft: Статья, является черновиком
    :param browser: Драйвер вэб-браузера
    :param live_server_url: корневой адрес веб-приложения
    :param description: Добавить описание. Опциональный. По умолчанию const.TEST_GUIDE_DESCRIPTION.
    При None - без описания
    :param cover_path: Путь к обложке Руководства. Опциональный. По умолчанию const.TEST_GUIDE_COVER_IMG_PATH.
    При None - без обложки
    :return: кортеж из тест-страницы Руководства DetailGuidePage, Руководства Guide, пользователя CustomUser
    """
    user = create_user_and_pre_authenticated_session(browser, live_server_url)
    guide = create_guide(user, description=description, cover_path=cover_path)
    detail_guide_page = DetailGuidePage(browser, live_server_url, guide.pk)
    detail_guide_page.go_to_page()
    return detail_guide_page, guide, user


def create_guide(author: CustomUser, name: str = TEST_GUIDE_NAME,
                 description: Optional[str] = TEST_GUIDE_DESCRIPTION,
                 cover_path: Optional[str] = TEST_GUIDE_COVER_IMG_PATH) -> Guide:
    """Создает Руководство с автором author, названием name, описанием description и обложкой, расположенной
    по пути cover_path. Если не задавать параметры name, description, cover_path, то будут испозованы тестовые
    значения поумолчанию"""
    guide = Guide.objects.create(name=name,
                                 description=description,
                                 author=author)
    if cover_path:
        guide.cover = SimpleUploadedFile(cover_path,
                                         content=open(settings.BASE_DIR / cover_path, 'rb').read(),
                                         content_type='image/jpeg')
        guide.save()
    return guide


def create_user(username: str = TEST_USERNAME, password: str = TEST_PASSWORD,
                first_name: str = TEST_FIRST_NAME, last_name: str = TEST_LAST_NAME,
                is_superuser: bool = False) -> CustomUser:
    """
    Создать пользователя.
       Все аргументы могут быть опущены. Что приведет к созданию тестового пользователя по-умолчанию
    """
    user_model = get_user_model()
    user = user_model.objects.create(username=username,
                                     first_name=first_name,
                                     last_name=last_name
                                     )
    user.set_password(password)
    user.is_superuser = is_superuser
    user.save()
    return user


def create_user_and_pre_authenticated_session(browser: WebDriver,
                                              live_server_url: str,
                                              username: str = TEST_USERNAME,
                                              password: str = TEST_PASSWORD,
                                              first_name: str = TEST_FIRST_NAME,
                                              last_name: str = TEST_LAST_NAME, ) -> CustomUser:
    """
    Создать пользователя и аутентифицированную сессию
        Все аргументы могут быть опущены. Что приведет к созданию тестового пользователя по-умолчанию
    """
    # First, create a new test user
    user = create_user(username, password, first_name, last_name)

    user = create_pre_authenticated_session(browser, live_server_url, user)

    # # Then create the authenticated session using the new user credentials
    # session = SessionStore()
    # session[SESSION_KEY] = user.pk
    # session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    # session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    # session.save()
    #
    # browser.get(live_server_url + '/404_no_such_url/')
    #
    # cookie = {
    #     'name': settings.SESSION_COOKIE_NAME,
    #     'value': session.session_key,
    #     'secure': False,
    #     'path': '/',
    # }
    #
    # browser.add_cookie(cookie)

    return user


def create_pre_authenticated_session(browser: WebDriver,
                                     live_server_url: str,
                                     user: CustomUser) -> CustomUser:
    """Создаёт аутентифицированную сессию для пользователя user"""

    # Then create the authenticated session using the new user credentials
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()

    browser.get(live_server_url + '/404_no_such_url/')

    cookie = {
        'name': settings.SESSION_COOKIE_NAME,
        'value': session.session_key,
        'secure': False,
        'path': '/',
    }

    browser.add_cookie(cookie)

    return user