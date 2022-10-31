from typing import Optional
from selenium.webdriver.common.by import By
import selenium.common.exceptions

from functional_tests.base import FunctionalTest
from selenium.webdriver.remote.webdriver import WebElement


class InputField(object):
    """Поле ввода"""

    def __init__(self, test: FunctionalTest, _field_id: str):
        self._browser = test.browser
        self._field_id = _field_id

    @property
    def _field(self) -> Optional[WebElement]:
        """само поле ввода"""
        try:
            return self._browser.find_element(By.ID, self._field_id)
        except selenium.common.exceptions.NoSuchElementException:
            return None

    @property
    def value(self) -> Optional[str]:
        """значение написанное внутри поля ввода"""
        if self._field:
            return self._field.get_attribute('value')
        else:
            return None

    @property
    def error_message(self) -> Optional[WebElement]:
        """следуемая за полем ввода ошибка"""
        if self._field:
            return self._field.find_element(By.XPATH, "./following-sibling::div[@class='invalid-feedback']")
        else:
            return None

    @property
    def label(self) -> Optional[WebElement]:
        """Лэйбл, находящийся перед полем"""
        try:
            return self._browser.find_element(
                By.CSS_SELECTOR,
                f"#content label[for='{self._field_id}']"
            )
        except selenium.common.exceptions.NoSuchElementException:
            return None

    @property
    def help_text(self) -> Optional[str]:
        """следуемая за полем подсказка"""
        if self._field:
            return self._field.find_element(By.XPATH, "./following-sibling::div[@class='help']").text
        else:
            return None

    @property
    def placeholder(self) -> Optional[str]:
        """Плейсхолдер поля"""
        if self._field:
            return self._field.get_attribute("placeholder")
        else:
            return None

    def is_invalid(self) -> bool:
        """поле ввода не валидно?"""
        if self._field:
            return 'is-invalid' in self._field.get_attribute("class").split()
        else:
            return False

    def is_displayed(self) -> bool:
        """поле ввода видимо?"""
        if self._field:
            return self._field.is_displayed()
        else:
            return False

    def send_keys(self, keys: str) -> None:
        """нажать в поле ввода соответствующие кнопки"""
        if self._field:
            self._field.send_keys(keys)

    def clear(self) -> None:
        """очищает данные в поле"""
        if self._field:
            self._field.clear()
