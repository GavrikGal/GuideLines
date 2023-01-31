import time
from typing import Optional
import selenium.common.exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ...base import wait


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

    @wait
    def wait_for(self, fn):
        """ожидать"""
        return fn()

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
    def _locator(self):
        """Локатор элемента"""
        try:
            if self._id:
                return (
                    By.ID,
                    self._id
                )
            elif self._name:
                return (
                    By.NAME,
                    self._name
                )
            else:
                return (
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
            # self._btn.location_once_scrolled_into_view

            # self._browser.execute_script("arguments[0].scrollIntoView(true);", self._btn)
            #
            # actions = ActionChains(self._browser)
            # actions.move_to_element(self._btn)
            # actions.perform()

            element = self._btn

            # desired_y = (element.size['height'] / 2) + element.location['y']
            # window_h = self._browser.execute_script('return window.innerHeight')
            # window_y = self._browser.execute_script('return window.pageYOffset')
            # current_y = (window_h / 2) + window_y
            # scroll_y_by = desired_y - current_y
            #
            # self._browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

            # self._browser.execute_script("arguments[0].scrollBy(0, 100)", element)

            # todo: рефакторинг без костылей
            self._browser.execute_script("arguments[0].scrollIntoView();", element)
            # WebDriverWait(self._browser, 5).until(EC.element_to_be_clickable(element)).click()

            WebDriverWait(self._browser, 10).until(EC.visibility_of_element_located(self._locator))
            # time.sleep(2)
            # actions = ActionChains(self._browser)
            # actions.move_to_element(self._btn).click().perform()

            self._btn.click()



            # self._browser.execute_script("arguments[0].click();", self._btn)
            # WebDriverWait(self._browser, 20).until(EC.element_to_be_clickable(self._btn)).click()

            # element.click()

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
