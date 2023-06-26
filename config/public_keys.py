# -*- coding: utf-8 -*-
"""
Настройки скрипта
"""
from dotenv import load_dotenv
import os
from sys import platform


# Ссылки
URL = 'https://portal.rfc-revizor.ru'
URL_AUTH = 'https://portal.rfc-revizor.ru/login/'
URL_CAPTCHA = 'https://portal.rfc-revizor.ru/captcha/{secretcodeId}'
URL_REPORTS_CREATE = 'https://portal.rfc-revizor.ru/cabinet/myclaims-reports/create'
URL_REPORTS = 'https://portal.rfc-revizor.ru/cabinet/myclaims-reports/'
URL_DOWNLOAD_REPORT = 'https://portal.rfc-revizor.ru/cabinet/claims-reports/download/{archive_id}.zip'

# Локаторы
XPATH_CAPTCHA_ID = '//*[@name="secretcodeId"]'
XPATH_CAPTCHA_SRC = '//*[@alt="captcha"]'
XPATH_HEADER = '//*[@class="watching list-table"]/thead/tr[1]/th'
XPATH_TABLE_ROW = '//*[@class="watching list-table"]/tbody/tr'
XPATH_MESSAGE_ERROR = '//*[contains(@class,"danger-inline")]'

# Папки
DIRECTORY_CAPTCHA = 'captcha_img'
DIRECTORY_ARCHIVE = 'report'
DIRECTORY_ARCHIVE_TEMP = f'{DIRECTORY_ARCHIVE}/tmp_{{archive_id}}'
DIRECTORY_DEBUG = 'log'
DIRECTORY_DATABASE = 'database'
DIRECTORY_CONFIG = 'config'

# Константы
SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Конфигурационные файлы
FILE_DEBUG = f'{DIRECTORY_DEBUG}/debug.log'
FILE_ENV = f'{DIRECTORY_CONFIG}/secret_keys.env'

# Секретные переменные окружения из env
load_dotenv(FILE_ENV)
TOKEN = os.getenv('TOKEN_BOT')
CIPHER_KEY = bytes(os.getenv('CIPHER_KEY'), 'utf-8')

# Файл БД согласно операционной системе
if platform in ['linux', 'linux2']:
    """ linux """
    FILE_DATABASE = f'/root/rkn/{DIRECTORY_DATABASE}/database.db'
elif platform == "darwin":
    """ OS X """
    pass
elif platform == "win32":
    """ Windows """
    FILE_DATABASE = f'{DIRECTORY_DATABASE}/database.db'
else:
    raise ValueError('Не определена операционная система и не получен файл БД')
