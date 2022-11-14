from typing import Optional
import selenium.common.exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.base import FunctionalTest


class BaseButton(object):
    """Базовая кнопка"""

    def __init__(self, test: FunctionalTest, type_: str = None,
                 section: str = '#content', class_: str = 'btn', id_: str = '', name: str = None):
        self._browser = test.browser
        self._type = type_
        self._section = section
        self._class = class_
        self._id = id_
        self._name = name

    @property
    def _btn(self) -> Optional[WebElement]:
        """сама кнопка"""
        try:
            if self._id:
                return self._browser.find_element(
                    By.ID,
                    self._id
                )
            elif self._name:
                return self._browser.find_element(
                    By.NAME,
                    self._name
                )
            else:
                return self._browser.find_element(
                    By.CSS_SELECTOR,
                    f"{self._section} form .{self._class}[type='{self._type}']"
                )
        except selenium.common.exceptions.NoSuchElementException:
            return None

    @property
    def label(self) -> Optional[str]:
        """Надпись на кнопке"""
        if self._btn:
            return self._btn.text
        else:
            return None

    def click(self) -> None:
        """Клик по кнопке"""
        if self._btn:
            self._btn.click()

    def hover(self) -> None:
        """Навести курсор на кнопку"""
        if self._btn:
            btn_block = self._btn.find_element(By.TAG_NAME, 'div')
            hover = ActionChains(self._browser).move_to_element(btn_block)
            hover.perform()

    def is_displayed(self) -> bool:
        """Кнопка видима?"""
        if self._btn:
            return self._btn.is_displayed()
        else:
            return False

    def send_keys(self, keys: str) -> None:
        """Отправить нажатие клавиш клавиатуры кнопке"""
        self._btn.send_keys(keys)


class SubmitButton(BaseButton):
    """Основная кнопка (отправка формы)"""

    def __init__(self, test: FunctionalTest):
        super().__init__(test, type_='submit')


class LogoutButton(BaseButton):
    """Копка выхода из системы"""

    def __init__(self, test: FunctionalTest):
        super().__init__(test, type_='submit', id_='logout-btn', section='header')


class LoginButton(BaseButton):
    """Копка выхода из системы"""

    def __init__(self, test: FunctionalTest):
        super().__init__(test, type_='submit', id_='login-btn', section='header')
