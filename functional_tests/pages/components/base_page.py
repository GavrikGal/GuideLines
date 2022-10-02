from selenium.webdriver.common.by import By


class BasePage(object):
    """Общие элементы для всех страниц"""

    def __init__(self, test, page_url=''):
        self.test = test
        self.page_url = page_url

    @property
    def page_title(self):
        """заголовок страницы"""
        page_title = self.test.browser.title
        return page_title

    @property
    def header(self):
        """получить элемент шапки"""
        header = self.test.browser.find_element(By.ID, 'header')
        return header

    def go_to_page(self):
        """перейти на страницу"""
        self.test.browser.get(self.test.live_server_url + self.page_url)
        # Подождать пока загрузится шапка
        self.test.assertIn(
            'GuideLines',
            self.page_title
        )
        return self
