from django.conf import settings
from django.urls import reverse
from selenium.webdriver.firefox.webdriver import WebDriver

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, BaseButton


class NewGuidePage(BasePage):
    """Страница нового Руководства"""

    def __init__(self, browser: WebDriver, live_server_url: str) -> None:
        super().__init__(browser, live_server_url, reverse('guides:new_guide'))  # установка адреса страницы
        self.guide_name_field = InputField(browser, 'id_name')
        self.description_field = InputField(browser, 'id_description')
        self.create_guide_btn = SubmitButton(browser)
        self.guide_cover_btn = BaseButton(browser, id_='id_cover')

    def set_cover_img(self, img_path: str) -> None:
        """Установка картинки обложки Руководства"""
        self.guide_cover_btn.send_keys(str(settings.BASE_DIR / img_path))
