from django.conf import settings
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.pages.components.base_page import BasePage
from functional_tests.pages.components.fields import InputField
from functional_tests.pages.components.buttons import SubmitButton, BaseButton


class EditGuidePage(BasePage):
    """Страница редактирования Руководства"""

    def __init__(self, browser: WebDriver, live_server_url: str, pk: int = 1) -> None:
        # установка адреса страницы, тестовый pk=1
        super().__init__(browser, live_server_url, reverse('guides:edit_guide', kwargs={'pk': pk}))
        self.guide_name_field = InputField(browser, 'id_name')
        self.description_field = InputField(browser, 'id_description')
        self.save_guide_btn = SubmitButton(browser)
        self.guide_cover_btn = BaseButton(browser, id_='id_cover')

    def set_cover_img(self, img_path: str) -> None:
        """Установка картинки обложки Руководства"""
        self.guide_cover_btn.send_keys(str(settings.BASE_DIR / img_path))

    @property
    def guide_cover(self) -> WebElement:
        """Обложка Руководства"""
        return self._browser.find_element(By.ID, 'guide').find_element(By.TAG_NAME, 'img')

