# -*- coding: utf-8 -*-
"""
Функции по шифрованию/дешифрованию сообщений
"""

from src.core.config import settings
from loguru import logger

from cryptography.fernet import Fernet
from typing import Union


class Common:
    ERROR_CONVERT = 'Невозможно конвертировать тип сообщения! Допустимо: bytes, int, str! Сообщение "{}" имеет тип "{}"'
    MSG_ENCRYPT = 'Сообщение зашифровано!'
    MSG_DECRYPT = 'Сообщение расшифровано!'


class Cryptography(Common):

    @staticmethod
    def generate_obj_fernet(password: bytes = settings.env.cipher_key) -> Fernet:
        """ Генерация объекта класса Fernet

        Args:
            password: пароль для генерации ключа шифрования
        """
        return Fernet(password)

    @staticmethod
    def type_conversion(message: Union[bytes, int, str]):
        """ Конвертация строки в байтовую строку или строку UTF-8 """
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        elif isinstance(message, str or int):
            message = bytes(message, encoding='utf-8')
        else:
            logger.error(Common.ERROR_CONVERT.format(message, type(message)))

        return message

    def custom_encrypt(self, message: str) -> str:
        """ Шифруем """
        message_str_to_bytes = self.type_conversion(message=message)
        message_bytes = self.generate_obj_fernet().encrypt(message_str_to_bytes)
        message_bytes_to_str = self.type_conversion(message=message_bytes)
        if isinstance(message_bytes_to_str, str):
            logger.info(Common.MSG_ENCRYPT)
        return message_bytes_to_str

    def custom_decrypt(self, encrypted_text: str) -> str:
        """ Расшифровываем """
        encrypted_str_to_bytes = self.type_conversion(message=encrypted_text)
        encrypted_bytes = self.generate_obj_fernet().decrypt(encrypted_str_to_bytes)
        encrypted_bytes_to_str = self.type_conversion(message=encrypted_bytes)
        if isinstance(encrypted_bytes_to_str, str):
            logger.info(Common.MSG_DECRYPT)
        return encrypted_bytes_to_str
