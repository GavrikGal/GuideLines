from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from functional_tests.pages.components.buttons import LogoutButton, LoginButton


class BasePage(object):
    """Общие элементы для всех страниц"""

    def __init__(self, browser: WebDriver, live_server_url: str, page_url: str = ''):
        self._browser = browser
        self.page_url = page_url
        self.live_server_url = live_server_url
        self.login_btn = LoginButton(self._browser)
        self.logout_btn = LogoutButton(self._browser)

    @property
    def page_title(self) -> str:
        """заголовок страницы"""
        page_title = self._browser.title
        return page_title

    @property
    def header(self) -> WebElement:
        """получить элемент шапки"""
        header = self._browser.find_element(By.ID, 'header')
        return header

    @property
    def tooltip(self) -> WebElement:
        """всплывающая подсказка bootstrap tooltip, появляющаяся при наведении на какой-либо элемент"""
        return self._browser.find_element(By.CLASS_NAME, 'tooltip')

    def go_to_page(self) -> 'BasePage':
        """перейти на страницу"""
        self._browser.get(self.live_server_url + self.page_url)
        # Подождать пока загрузится страница
        timeout = 2
        try:
            element_present = EC.presence_of_element_located((By.ID, 'content'))
            WebDriverWait(self._browser, timeout).until(element_present)
        except TimeoutException as err:
            msg = 'Не могу загрузить страницу [' + self.live_server_url + self.page_url + ']'
            err.msg = msg
            raise

        return self

    def is_text_present(self, text) -> bool:
        """Найти текст на странице"""
        try:
            if text in self._browser.find_element(By.XPATH, f"//*[text()='{text}']").text:
                return True
            else:
                return False
        except NoSuchElementException:
            return False
