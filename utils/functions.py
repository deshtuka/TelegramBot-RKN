# -*- coding: utf-8 -*-
"""
Основные функции для работы скрипта
"""
from typing import Union

from config import public_keys
from utils import logger

from lxml import html
import re
import os
from zipfile import ZipFile
import csv


def get_secretcodeid_from_captcha_on_login_page(response):
    """ Функция получения secretcodeId со страницы авторизации

    Args:
        response: тело ответа

    Returns:
        secret_code: число secretcodeId
    """

    secret_code = None

    if response.status_code == 200:

        tree_content = html.fromstring(response.content)

        secret_code_obj = tree_content.xpath(public_keys.XPATH_CAPTCHA_ID)
        secret_code = [str(obj.attrib['value']) for obj in secret_code_obj][0]

    return secret_code


def save_file_from_request(response, archive_id: str) -> tuple:
    """ Сохранение архива в директорию из полученного тела ответа

    Args:
        response: тело ответа. Объект класса requests.Response
        archive_id: название архива (id ссылки). Пример: 9076995.zip

    Returns:
        True/False: Успешно или нет скачан файл
        file_full_name: полный путь до файла
    """
    file_full_name = f'{public_keys.DIRECTORY_ARCHIVE}/{archive_id}.zip'

    with open(file_full_name, 'wb') as archive:
        archive.write(response.content)

    if os.path.exists(file_full_name):
        return True, file_full_name
    else:
        return False, file_full_name


@logger.log_time('Парсинг страницы "Авторизация"')
def scraping_page_auth(response):
    """ Функция парсинга страницы авторизации на наличие ошибок

    Args:
        response: тело ответа
    """
    result_bool, messages = False, 'Ошибка данных авторизации!'

    if response.status_code == 200:
        tree_content = html.fromstring(response.content)

        messages_obj = tree_content.xpath(public_keys.XPATH_MESSAGE_ERROR)
        messages_list = [str(obj.text) for obj in messages_obj]

        if len(messages_list) > 0:
            return False, '\n'.join(messages_list)
        else:
            return True, 'Успешно!'

    return result_bool, messages


@logger.log_time('Парсинг страницы "Мои отчеты"')
def scraping_page_my_reports(response) -> Union[dict, str]:
    """ Функция парсинга страницы "мои отчеты"

    Args:
        response: тело ответа
    """
    result_dict = dict()
    xpath_table_row = public_keys.XPATH_TABLE_ROW

    # [<Response [302]>] - history[0].status_code
    if response.status_code == 200:
        tree_content = html.fromstring(response.content)

        table_row = tree_content.xpath(xpath_table_row)

        for index, row in enumerate(table_row):
            date_create = [obj.text for obj in row.xpath(f'{xpath_table_row}//td[1]')][index]
            date_report = [obj.text for obj in row.xpath(f'{xpath_table_row}//td[2]')][index]
            request_status = [obj.text for obj in row.xpath(f'{xpath_table_row}//td[4]')][index].split(" ")[-1]
            try:
                link = [str(obj.attrib["href"]) or obj.text for obj in row.xpath(f'{xpath_table_row}//a')][index]
            except IndexError:
                link = ''

            download_id = ''.join(re.findall(r'\d', link))

            # Оптимизация вывода даты создания: "27.03.2022 09:41" -> "27.03 09:41"
            date, time = date_create.split(' ')
            new_date = '.'.join(date.split('.')[:2])
            date_create = f'{new_date} {time}'

            # Наполнение словаря
            result_dict[f'{index}_{date_report}_{download_id}'] = f'{date_create} ({date_report}) -> {request_status}'
        return result_dict
    return 'Страница "Мои отчеты" - не получена'


def unpacking_archive(archive_id: str, path_archive: str) -> tuple:
    """Распаковка и получение файлов из архива

    Args:
        archive_id: id архива. Пример: "9076995"
        path_archive: путь до архива. Пример: "report/9076995.zip"

    Returns:
        path_to_files: полный путь до файлов PDF и CSV во временной папке
        message_from_csv: формулировка из CSV файла
    """
    tmp_dir = public_keys.DIRECTORY_ARCHIVE_TEMP.format(archive_id=archive_id)

    # Распаковка архива
    with ZipFile(path_archive, 'r') as zip_file:
        zip_file.extractall(tmp_dir)

    # Удаление архива
    os.remove(path_archive)

    # Полное название файлов в папке
    files_name_list = os.listdir(tmp_dir)
    file_pdf = [one for one in files_name_list if one.endswith('.pdf')][0]
    file_csv = [one for one in files_name_list if one.endswith('.csv')][0]

    # Полный путь файла во временной папке
    path_to_files = (
        f'{tmp_dir}/{file_csv}',
        f'{tmp_dir}/{file_pdf}'
    )

    # Парсинг CSV
    message_from_csv = scraping_csv(path_to_csv=path_to_files[0])

    return path_to_files, message_from_csv


def scraping_csv(path_to_csv: str) -> str:
    # Парсинг CSV
    try:
        with open(path_to_csv, newline='', encoding='cp1251') as file:
            reader = csv.reader(file)
            # Каждая строка это список
            list_row_text = [row for row in reader]

            # Проверяем, что отчет содержит полезные данные
            if len(list_row_text) < 5:
                return 'Error - ошибка с отчетом'

            if len(list_row_text) == 5:
                return list_row_text[-1][0]

            # Извлекаем данные без процента
            set_percent, count_error = set(), 0
            for row in list_row_text[6:]:
                if len(row) > 0 and row[0].count(";") == 2:
                    re_percent = ''.join(re.findall(r'[<|>|\d]', row[0].split(';')[2]))
                    if re_percent:
                        set_percent.add(re_percent)

                if row[0].split(';')[0] == 'Всего':
                    count_error = int(row[0].split(';')[1])
                    break

            # Определяем качество отчета (по В)
            if '<1' in set_percent and len(set_percent) == 1:
                # Качество (по А)
                return f'А = {count_error}' if count_error > 10 else 'ОК'
            else:
                return f'А = {count_error}' if count_error > 10 else f'B = {set_percent}'

    except Exception as ex:
        logger.logger.error(f'Ошибка в парсинге CSV: {ex}')
        return 'Какая-то ошибка есть в отчете!'
