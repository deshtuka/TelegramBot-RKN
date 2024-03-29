﻿# -*- coding: utf-8 -*-
"""
Настройки проекта
"""
import os

from pydantic import BaseModel, BaseSettings, Field, AnyHttpUrl


# Абсолютный путь до каталога проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Url(BaseModel):
    """Ссылки"""
    _base_url:          AnyHttpUrl = 'https://portal.rfc-revizor.ru'
    auth:               AnyHttpUrl = f'{_base_url}/login/'
    captcha:            AnyHttpUrl = f'{_base_url}/captcha/{{secretcodeId}}'
    reports_create:     AnyHttpUrl = f'{_base_url}/cabinet/myclaims-reports/create'
    reports:            AnyHttpUrl = f'{_base_url}/cabinet/myclaims-reports/'
    download_report:    AnyHttpUrl = f'{_base_url}/cabinet/claims-reports/download/{{archive_id}}.zip'


class Xpath(BaseModel):
    """Локаторы"""
    captcha_id:     str = '//*[@name="secretcodeId"]'
    table_row:      str = '//*[@class="watching list-table"]/tbody/tr'
    message_error:  str = '//*[contains(@class,"danger-inline")]'


class Directory(BaseModel):
    """Каталоги проекта"""
    temp:           str = f'{BASE_DIR}/temp'
    captcha:        str = f'{temp}/captcha_img'
    archive:        str = f'{temp}/report'
    archive_temp:   str = f'{archive}/tmp_{{archive_id}}'
    debug:          str = f'{BASE_DIR}/log'
    database:       str = f'{BASE_DIR}/database'


class File(BaseModel):
    """Конфигурационные файлы"""
    debug:      str = f'{Directory().debug}/debug.log'
    env:        str = f'{BASE_DIR}/secret_keys.env'
    database:   str = f'{Directory().database}/database.db'


class Constants(BaseModel):
    """Константы"""
    sql_datetime_format = '%Y-%m-%d %H:%M:%S'


class Env(BaseSettings):
    """Секретные переменные окружения из env"""

    token: str = Field('Test', env="TOKEN_BOT")
    cipher_key: bytes = Field('Test', env="CIPHER_KEY")

    chat_id_admin: int = Field(0, env="CHAT_ID_ADMIN")

    redis_host: str = Field('redis', env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    vm_host: str = Field('host.docker.internal', env="VICTORIAMETRICS_HOST")
    vm_port: int = Field(8428, env="VICTORIAMETRICS_PORT")

    class Config:
        env_file = File().env
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    url = Url()
    xpath = Xpath()
    dir = Directory()
    file = File()
    const = Constants()
    env = Env()


settings = Settings()
