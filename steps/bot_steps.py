# -*- coding: utf-8 -*-
"""
Бизнес логика телеграм бота
"""

from request_api.request_api import ApiRequests
from steps import bot_asserts
from utils import functions, file, folders, logger
from utils.crypto import Cryptography
from config.public_keys import URL_CAPTCHA, DIRECTORY_CAPTCHA, URL_DOWNLOAD_REPORT, DIRECTORY_ARCHIVE_TEMP
from bot import BotDatabase
from config.bot_message import Message

from typing import Tuple, Union

request = ApiRequests()


def is_check_cookie(chat_id: int) -> tuple:
    """Проверка сохраненных данных сессии.

    Args:
        chat_id: идентификатор чата пользователя с ботом

    Returns:
        True/False: активная сессия
        cookies: куки из файла
        user_agent: агент из файла
        secret_code_id: секрет код
    """
    status, level, msg = False, 'WARNING', Message.COOKIES_BAD

    # Получение данных из БД
    user_agent, secret_code_id, cookies = BotDatabase.get_session(chat_id=chat_id)

    if bot_asserts.is_cookie_active_less_than_25_min(chat_id=chat_id):
        if user_agent is not None and cookies is not None:
            status, level, msg = True, 'SUCCESS', Message.COOKIES_GOOD

    logger.logger.log(level, msg)
    return status, cookies, user_agent, secret_code_id


def get_captcha(chat_id: int) -> ...:
    """ Получение Капчи

    Returns:
        None-Ошибка на сайте; Path-Капча скачана
    """
    index = 0

    while index < 5:
        # GET-запрос к странице авторизации
        response = request.get_authorization_page()

        secret_code_id = functions.get_secretcodeid_from_captcha_on_login_page(response=response)
        img_url = URL_CAPTCHA.format(secretcodeId=secret_code_id)

        # Получение CookieJar и сохранение Dict как str -> "{'key': 'value'}"
        cookies = str(request.requests.utils.dict_from_cookiejar(response.cookies))
        user_agent = str({'User-Agent': response.request.headers['User-Agent']})

        # Сохранение в БД (куков, secretcodeId, user-agent)
        BotDatabase.edit_cookies(chat_id=chat_id, cookies=cookies)
        BotDatabase.edit_secret_code_id(chat_id=chat_id, secret_code_id=secret_code_id)
        BotDatabase.edit_user_agent(chat_id=chat_id, user_agent=user_agent)

        # GET-запрос на сохранение картинки с капчей
        file_name = f'{DIRECTORY_CAPTCHA}/{secret_code_id}.png'
        response = request.get_download_captcha(url=img_url, cookies=response.cookies)
        if file.save_image_from_request_body(response=response, file_name=file_name):
            break
        index += 1
    else:
        file_name = None

    return file_name


def bot_get_captcha(bot, chat_id: int):
    """ Получение картинки капчи со страницы авторизации + вывод в чат

    Args:
        bot: экземпляр бота
        chat_id: идентификатор чата пользователя с ботом
    """
    file_name_captcha = get_captcha(chat_id=chat_id)

    if file_name_captcha is None:
        bot.send_message(chat_id, bot.msg.ERROR_CAPTCHA)
    else:
        with open(file_name_captcha, 'rb') as image:
            bot.send_photo(chat_id, image)
        # Удаление изображения капчи из памяти после отправки в чат
        file.remove(file_name_captcha)


def authorization(secret_code_status: int, chat_id: int) -> Tuple[bool, str]:
    """ Авторизация на сайте """
    # Получение данных из БД
    login, password_encoded = BotDatabase.get_login_password(chat_id=chat_id)
    if not login or not password_encoded:
        return False, Message.INFO_SETTING

    user_agent, secret_code_id, cookies = BotDatabase.get_session(chat_id=chat_id)

    # Запрос авторизации
    response = request.post_authorization(login=login,
                                          password=Cryptography().custom_decrypt(encrypted_text=password_encoded),
                                          headers=user_agent,
                                          cookies=cookies,
                                          secret_code_status=secret_code_status,
                                          secret_code_id=secret_code_id)

    # Проверка ошибок учетной записи
    is_auth, msg_auth = functions.scraping_page_auth(response)

    if is_auth:
        BotDatabase.add_last_action(chat_id=chat_id)

    return is_auth, msg_auth


def page_report(chat_id: int) -> Union[dict, str]:
    """Получение информации о состояние отчетов

    Returns:
         Словарь спарсенных данных отчетов для вывода в кнопки
    """
    user_agent, _, cookies = BotDatabase.get_session(chat_id=chat_id)

    response = request.get_page_report(headers=user_agent, cookies=cookies)

    # Парсинг
    result = functions.scraping_page_my_reports(response)
    if isinstance(result, dict) and len(result) > 0:
        BotDatabase.add_last_action(chat_id=chat_id)
    return result


def create_report_for_date(chat_id: int, date: str) -> bool:
    """Создание заявки на дату

    Args:
        chat_id: идентификатор чата пользователя с ботом
        date: дата на которую создать отчет

    Returns:
         True/False - в зависимости от ответа запроса
    """
    is_cookie, cookies, user_agent, _ = is_check_cookie(chat_id=chat_id)

    if is_cookie:
        response = request.post_create_report(date=date, headers=user_agent, cookies=cookies)
        if response.status_code == 200:
            BotDatabase.add_last_action(chat_id=chat_id)
            return True
    return False


def download_the_selected_report(chat_id: int, archive_id: str):
    """Скачивание архива выбранного отчета

    Args:
        chat_id: идентификатор чата пользователя с ботом
        archive_id: название архива (id ссылки). Пример: 9076995.zip

    Returns:
        True/False: результат наличия архива на ПК
    """
    # Проверяем сессию
    is_cookie, cookies, user_agent, _ = is_check_cookie(chat_id=chat_id)

    if is_cookie:
        # Создаем ссылку -> url
        url_download = URL_DOWNLOAD_REPORT.format(archive_id=archive_id)

        # GET-запрос на скачивание отчета
        response = request.get_save_file_on_pc(url=url_download, headers=user_agent, cookies=cookies)

        # Получение из тела ответа архива отчета
        is_archive, path_archive = functions.save_file_from_request(response=response, archive_id=archive_id)

        if is_archive:
            # Создание временной папки
            folders.create(path_dirs=DIRECTORY_ARCHIVE_TEMP.format(archive_id=archive_id))
            # Распаковка архива
            path_to_files, message_from_csv = functions.unpacking_archive(archive_id=archive_id,
                                                                          path_archive=path_archive)

            BotDatabase.add_last_action(chat_id=chat_id)
            return True, message_from_csv, path_to_files
        else:
            return False, Message.ERROR_DOWNLOAD, ''
    else:
        return False, Message.ERROR_AUTH, ''
