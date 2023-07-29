# -*- coding: utf-8 -*-
"""
Функции для работы с файлами
"""
import os

import requests

from loguru import logger


def save_image_from_request_body(response: requests.Response, file_name: str) -> bool:
    """Сохранение изображения из тела запроса

    Args:
        response: тело ответа
        file_name: полное название сохраняемого файла

    Returns:
        bool: результат сохранения файла.
    """
    if response.status_code == 200:
        with open(file_name, 'wb') as image:
            image.write(response.content)
            logger.info(f'Файл "{file_name}" сохранен!')
        return True
    else:
        logger.error(f'Файл "{file_name}" не сохранен! Статус ответа: {response.status_code}')
        return False


def remove(path: str) -> ...:
    """Удаление файла

    Args:
          path: полный путь файла
    """
    try:
        os.remove(path)
    except FileNotFoundError:
        logger.warning(f'Файл "{path}" - не найден')
    except PermissionError:
        logger.error(f'Файл "{path}" - отказано в доступе')
    except OSError:
        logger.error(f'Файл "{path}" - ошибка операции ввода-вывода')
    else:
        logger.trace(f'Файл "{path}" - удален')
