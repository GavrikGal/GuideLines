from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class BaseButton(object):
    """Базовая кнопка"""

    def __init__(self, test: FunctionalTest, type_: str = None,
                 section: str = '#content', class_: str = 'btn', id_: str = ''):
        self._browser = test.browser
        self._type = type_
        self._section = section
        self._class = class_
        self._id = id_

    @property
    def _btn(self):
        """сама кнопка"""
        if self._id:
            return self._browser.find_element(
                By.ID,
                self._id
            )
        else:
            return self._browser.find_element(
                By.CSS_SELECTOR,
                f"{self._section} form .{self._class}[type='{self._type}']"
            )

    @property
    def label(self):
        """Надпись на кнопке"""
        return self._btn.text

    def click(self):
        """Клик по кнопке"""
        return self._btn.click()

    def is_displayed(self):
        """Кнопка видима?"""
        return self._btn.is_displayed()


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
