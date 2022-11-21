import selenium.common.exceptions

from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement


class BasePanel(object):
    """Базовый класс для панелей"""

    def __init__(self, browser: WebDriver, _panel_id: str):
        self._browser = browser
        self._panel_id = _panel_id

    @property
    def _panel(self) -> Optional[WebElement]:
        """Сама панель"""
        try:
            return self._browser.find_element(By.ID, self._panel_id)
        except selenium.common.exceptions.NoSuchElementException:
            return None

    def is_displayed(self):
        """Панель видима?"""
        if self._panel:
            return self._panel.is_displayed()
        else:
            return False
