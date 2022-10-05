from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from selenium.webdriver.remote.webdriver import WebElement


class InputField(object):
    """Поле ввода"""

    def __init__(self, test: FunctionalTest, _field_id: str):
        self._browser = test.browser
        self._field_id = _field_id

    @property
    def _field(self) -> WebElement:
        """само поле ввода"""
        return self._browser.find_element(By.ID, self._field_id)

    @property
    def value(self) -> str:
        """значение написанное внутри поля ввода"""
        return self._field.get_attribute('value')

    @property
    def error_message(self) -> WebElement:
        """следуемая за полем ввода ошибка"""
        return self._field.find_element(By.XPATH, "./following-sibling::div[@class='invalid-feedback']")

    @property
    def label(self) -> WebElement:
        """Лэйбл, находящийся перед полем"""
        return self._browser.find_element(
            By.CSS_SELECTOR,
            f"#content label[for='{self._field_id}']"
        )

    @property
    def help_text(self) -> str:
        """следуемая за полем подсказка"""
        return self._field.find_element(By.XPATH, "./following-sibling::div[@class='help']").text

    @property
    def placeholder(self) -> str:
        """Плейсхолдер поля"""
        return self._field.get_attribute("placeholder")

    def is_invalid(self) -> bool:
        """поле ввода не валидно?"""
        return 'is-invalid' in self._field.get_attribute("class").split()

    def is_displayed(self) -> bool:
        """поле ввода видимо?"""
        return self._field.is_displayed()

    def send_keys(self, keys: str) -> None:
        """нажать в поле ввода соответствующие кнопки"""
        self._field.send_keys(keys)

    def clear(self) -> None:
        """очищает данные в поле"""
        self._field.clear()
