from typing import Optional
import selenium.common.exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseButton(object):
    """Базовая кнопка"""

    def __init__(self, browser: WebDriver, type_: str = None,
                 section: str = '#content', class_: str = 'btn', id_: str = '', name: str = None):
        self._browser = browser
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
            # self._btn.click()
            # print(self._btn.location_once_scrolled_into_view)
            self._browser.execute_script("arguments[0].scrollIntoView();", self._btn)
            WebDriverWait(self._browser, 20).until(EC.element_to_be_clickable(self._btn)).click()

    def hover(self) -> None:
        """Навести курсор на кнопку"""
        if self._btn:
            hover = ActionChains(self._browser).move_to_element(self._btn)
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

    def __init__(self, browser: WebDriver):
        super().__init__(browser, type_='submit')


class LogoutButton(BaseButton):
    """Копка выхода из системы"""

    def __init__(self, browser: WebDriver):
        super().__init__(browser, type_='submit', id_='logout-btn', section='header')


class LoginButton(BaseButton):
    """Копка выхода из системы"""

    def __init__(self, browser: WebDriver):
        super().__init__(browser, type_='submit', id_='login-btn', section='header')
