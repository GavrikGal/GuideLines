from selenium.webdriver.common.by import By


class InputField(object):
    """Поле ввода"""

    def __init__(self, test, _field_id):
        self.test = test
        self._field_id = _field_id

    @property
    def _field(self):
        """само поле ввода"""
        return self.test.browser.find_element(By.ID, self._field_id)

    @property
    def value(self):
        """значение написанное внутри поля ввода"""
        return self._field.get_attribute('value')

    @property
    def error_message(self):
        """следуемая за полем ввода ошибка"""
        return self._field.find_element(By.XPATH, "./following-sibling::div[@class='invalid-feedback']")

    @property
    def label(self):
        """Лэйбл, находящийся перед полем"""
        return self.test.browser.find_element(
            By.CSS_SELECTOR,
            f"#content label[for='{self._field_id}']"
        )

    @property
    def help_text(self):
        """следуемая за полем подсказка"""
        return self._field.find_element(By.XPATH, "./following-sibling::div[@class='help']").text

    @property
    def placeholder(self):
        """Плейсхолдер поля"""
        return self._field.get_attribute("placeholder")

    def is_invalid(self):
        """поле ввода не валидно?"""
        return 'is-invalid' in self._field.get_attribute("class").split()

    def is_displayed(self):
        """поле ввода видимо?"""
        return self._field.is_displayed()

    def send_keys(self, keys):
        """нажать в поле ввода соответствующие кнопки"""
        return self._field.send_keys(keys)

    def clear(self):
        """очищает данные в поле"""
        return self._field.clear()