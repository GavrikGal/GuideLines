from selenium.common.exceptions import NoSuchElementException

from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement

from functional_tests.utils.const import (ARTICLE_DRAFT_LABEL)


class BaseCard(object):
    """Базовый класс для карточек"""

    def __init__(self, browser: WebDriver, card_id: str):
        self._browser = browser
        self.card_id = card_id

    @property
    def card(self) -> Optional[WebElement]:
        """Сама карточка"""
        try:
            return self._browser.find_element(By.ID, self.card_id)
        except NoSuchElementException:
            return None

    def click(self) -> None:
        """Клик по карточке"""
        if self.card:
            self.card.click()

    def is_displayed(self) -> bool:
        """Карточка видима?"""
        if self.card:
            return self.card.is_displayed()
        else:
            return False

    def is_draft(self) -> bool:
        """Карточка являеется черновиком"""
        if self.card:
            try:
                if ARTICLE_DRAFT_LABEL in self.card.find_element(By.XPATH, f"//*[text()='{ARTICLE_DRAFT_LABEL}']").text:
                    return True
                else:
                    return False
            except NoSuchElementException:
                return False
        else:
            return False

    def is_text_present(self, text) -> bool:
        """Найти текст на карточке"""
        try:
            if text in self.card.find_element(By.XPATH, f"//*[text()='{text}']").text:
                return True
            else:
                return False
        except NoSuchElementException:
            return False
