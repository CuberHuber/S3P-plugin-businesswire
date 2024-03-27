"""
Нагрузка плагина SPP

1/2 документ плагина
"""
import datetime
import logging
import re
import time
from random import uniform

import dateparser
import dateutil.parser
import pytz
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.spp.types import SPP_document


class BusinessWire:
    """
    Класс парсера плагина SPP

    :warning Все необходимое для работы парсера должно находится внутри этого класса

    :_content_document: Это список объектов документа. При старте класса этот список должен обнулиться,
                        а затем по мере обработки источника - заполняться.


    """

    SOURCE_NAME = 'businesswire'
    HOST = 'https://www.businesswire.com/portal/site/home/news/'
    utc = pytz.UTC
    date_begin = utc.localize(datetime.datetime(2023, 12, 6))
    _content_document: list[SPP_document]

    def __init__(self, webdriver, max_count_documents: int = None, last_document: SPP_document = None, *args, **kwargs):
        """
        Конструктор класса парсера

        По умолчанию внего ничего не передается, но если требуется (например: driver селениума), то нужно будет
        заполнить конфигурацию
        """
        # Обнуление списка
        self._content_document = []
        self._driver = webdriver
        self._max_count_documents = max_count_documents
        self._last_document = last_document
        self._wait = WebDriverWait(self._driver, timeout=20)

        # Логер должен подключаться так. Вся настройка лежит на платформе
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Parser class init completed")
        self.logger.info(f"Set source: {self.SOURCE_NAME}")
        ...

    def content(self) -> list[SPP_document]:
        """
        Главный метод парсера. Его будет вызывать платформа. Он вызывает метод _parse и возвращает список документов
        :return:
        :rtype:
        """
        self.logger.debug("Parse process start")
        try:
            self._parse()
        except Exception as e:
            self.logger.debug(f'Parsing stopped with error: {e}')
        else:
            self.logger.debug("Parse process finished")
        return self._content_document

    def _parse(self, abstract=None):
        """
        Метод, занимающийся парсингом. Он добавляет в _content_document документы, которые получилось обработать
        :return:
        :rtype:
        """
        # HOST - это главная ссылка на источник, по которому будет "бегать" парсер
        self.logger.debug(F"Parser enter to {self.HOST}")

        self._driver.get(self.HOST)  # Открыть страницу со списком businesswire в браузере
        self._wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.bwNewsList')))

        while len(self._driver.find_elements(By.CLASS_NAME, 'pagingNext')) > 0:
            self._wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.bwNewsList')))
            el_list = self._driver.find_element(By.CLASS_NAME, 'bwNewsList').find_elements(By.TAG_NAME, 'li')
            for el in el_list:
                try:
                    article_link = el.find_element(By.CLASS_NAME, 'bwTitleLink')
                    web_link = article_link.get_attribute('href')
                    title = article_link.text
                    pub_date = dateparser.parse(el.find_element(By.TAG_NAME, 'time').get_attribute('datetime'))
                    self._driver.execute_script("window.open('');")
                    self._driver.switch_to.window(self._driver.window_handles[1])
                    time.sleep(uniform(0.1, 1.2))
                    self._driver.get(web_link)
                    self._wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.bw-release-story')))
                    text_content = self._driver.find_element(By.CLASS_NAME, 'bw-release-story').text
                except Exception as e:
                    self.logger.warning(f'The Article cannot be parsed. Error: {e}')
                else:
                    document = SPP_document(
                        None,
                        title=title,
                        abstract=abstract if abstract else None,
                        text=text_content,
                        web_link=web_link,
                        local_link=None,
                        other_data=None,
                        pub_date=pub_date,
                        load_date=None,
                    )
                    # Логирование найденного документа
                    self.find_document(document)
                    self._driver.close()
                    self._driver.switch_to.window(self._driver.window_handles[0])
                    time.sleep(uniform(0.3, 1))
            try:
                self._driver.get(self._driver.find_element(By.CLASS_NAME, 'pagingNext').find_element(By.TAG_NAME, 'a').get_attribute('href'))
            except:
                self.logger.info('Не найдено перехода на след. страницу. Завершение...')
                break

    def _initial_access_source(self, url: str, delay: int = 2):
        self._driver.get(url)
        self.logger.debug('Entered on web page ' + url)
        time.sleep(delay)
        self._agree_cookie_pass()

    def _agree_cookie_pass(self):
        """
        Метод прожимает кнопку agree на модальном окне
        """
        cookie_agree_xpath = '//*[@id="onetrust-accept-btn-handler"]'

        try:
            cookie_button = self._driver.find_element(By.XPATH, cookie_agree_xpath)
            if WebDriverWait(self._driver, 5).until(ec.element_to_be_clickable(cookie_button)):
                cookie_button.click()
                self.logger.debug(F"Parser pass cookie modal on page: {self._driver.current_url}")
        except NoSuchElementException as e:
            self.logger.debug(f'modal agree not found on page: {self._driver.current_url}')

    @staticmethod
    def _find_document_text_for_logger(doc: SPP_document):
        """
        Единый для всех парсеров метод, который подготовит на основе SPP_document строку для логера
        :param doc: Документ, полученный парсером во время своей работы
        :type doc:
        :return: Строка для логера на основе документа
        :rtype:
        """
        return f"Find document | name: {doc.title} | link to web: {doc.web_link} | publication date: {doc.pub_date}"

    def find_document(self, _doc: SPP_document):
        """
        Метод для обработки найденного документа источника
        """
        if self._last_document and self._last_document.hash == _doc.hash:
            raise Exception(f"Find already existing document ({self._last_document})")

        if self._max_count_documents and len(self._content_document) >= self._max_count_documents:
            raise Exception(f"Max count articles reached ({self._max_count_documents})")

        self._content_document.append(_doc)
        self.logger.info(self._find_document_text_for_logger(_doc))
