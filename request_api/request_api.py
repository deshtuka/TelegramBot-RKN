# -*- coding: utf-8 -*-
"""
Класс для работы с запросами/ответами
"""

import requests
from requests.cookies import RequestsCookieJar
from user_agent import generate_user_agent
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from config import public_keys
from utils import logger


class ApiRequests:
    """
    Обертка для библиотеки requests
    """

    def __init__(self):
        self.requests = requests
        self.headers = {'User-Agent': generate_user_agent(device_type="desktop", os='win', navigator='chrome')}
        self.timeout = 10
        urllib3.disable_warnings(category=InsecureRequestWarning)

    @logger.logger.catch()
    def send_request(
            self, url: str, method: str, headers=None, timeout=None, data=None, cookies=None
    ) -> requests.Response:
        """Отправить запрос.

        Args:
            url: url адрес для отправки запроса
            method: тип запроса. (POST, GET, PUT и т.д.)
            headers: заголовки запроса.
            timeout: время ожидания ответа от сервера в секундах.
            data: тело запроса.
            cookies: куки

        Returns:
            response: объект класса requests.Response.
        """
        response = None
        headers = self.headers if headers is None else {key: value for (key, value) in headers.items()}
        timeout = self.timeout if timeout is None else timeout

        try:
            response = self.requests.request(
                method=method,
                url=url,
                timeout=timeout,
                cookies=cookies,
                headers=headers,
                data=data,
                verify=False
            )
        except requests.exceptions.ConnectTimeout as error:
            logger.log_display(msg={f'Время ожидания запроса "{timeout}" от удаленного сервера истекло': error},
                               level='ERROR')
        except requests.exceptions.SSLError as error:
            logger.log_display(msg={'Ошибка сертификата': error}, level='ERROR')
        except requests.exceptions.RequestException as error:
            logger.log_display(msg={'Произошло неоднозначное исключение при обработке запроса': error}, level='ERROR')
        except Exception as error:
            logger.log_display(msg={'Ошибка при отправке запроса': error}, level='ERROR')
        else:
            logger.log_request_response(response=response)

        return response

    @logger.log_time('GET-запрос - Получение страницы авторизации')
    def get_authorization_page(self) -> requests.Response:
        """ Отправить GET-запрос для получения страницы авторизации

        Returns:
            response: объект класса requests.Response.
        """
        return self.send_request(url=public_keys.URL_AUTH, method='GET')

    @logger.log_time('GET-запрос - Сохранение капчи на компьютер')
    def get_download_captcha(self, url: str, cookies: RequestsCookieJar) -> requests.Response:
        """ Отправить GET-запрос для сохранения картинки в директорию

        Args:
            url: url адрес для отправки запроса
            cookies: куки

        Returns:
            response: объект класса requests.Response.
        """
        return self.send_request(url=url, method='GET', cookies=cookies)

    @logger.log_time('POST-запрос - Авторизация на сайте')
    def post_authorization(self, login: str, password: str, headers: dict, cookies: RequestsCookieJar,
                           secret_code_status: int, secret_code_id: int) -> requests.Response:
        """ Отправить POST-запрос для авторизация на сайте

        Args:
            login: логин учетной записи
            password: пароль учетной записи
            headers: заголовки
            cookies: кук сессии
            secret_code_status: код из капчи
            secret_code_id: номер файла капчи

        Return:
            response: объект класса requests.Response.
        """
        data = {
            'email': login,
            'password': password,
            'secretcodestatus': secret_code_status,
            'secretcodeId': secret_code_id
        }
        return self.send_request(url=public_keys.URL_AUTH, method='POST', headers=headers, data=data, cookies=cookies)

    @logger.log_time('GET-запрос - Получение информации о состояние отчетов')
    def get_page_report(self, headers: dict, cookies: dict) -> requests.Response:
        """ Отправить GET-запрос на получение информации о состояние отчетов

        Args:
            headers: заголовки
            cookies: кук сессии

        Return:
            Авторизованная сессия
        """
        return self.send_request(url=public_keys.URL_REPORTS, method='GET', headers=headers, cookies=cookies)

    @logger.log_time('POST-запрос - Создание заявки')
    def post_create_report(self, date: str, headers: dict, cookies: RequestsCookieJar) -> requests.Response:
        """ Отправить POST-запрос для авторизация на сайте

        Args:
            date: дата на которую создается отчет. Формат: 18.03.2022
            headers: заголовки
            cookies: кук сессии

        Return:
            response: объект класса requests.Response.
        """
        data = {
            'reportDate': date,  # Пример: 18.03.2022
            'onlyMyClaims': 1
        }
        return self.send_request(url=public_keys.URL_REPORTS_CREATE, method='POST', headers=headers, data=data, cookies=cookies)

    @logger.log_time('GET-запрос - Скачивание архива')
    def get_save_file_on_pc(self, url, headers: dict, cookies: RequestsCookieJar) -> requests.Response:
        """ Сохранение архива в директорию

        Args:
            url: url адрес для отправки запроса
            headers: заголовки
            cookies: кук сессии

        Returns:
            response: объект класса requests.Response.
        """
        return self.send_request(url=url, method='GET', headers=headers, cookies=cookies)
