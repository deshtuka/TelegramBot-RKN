# -*- coding: utf-8 -*-
"""
Функции для работы с каталогами
"""
import os
from typing import Union

from utils import file
from utils.logger import logger


def create(path_dirs: Union[str, dict]):
    """Создание каталога

    Args:
        path_dirs: путь до каталога или списка каталогов
    """
    directory = path_dirs.values() if isinstance(path_dirs, dict) else [path_dirs]

    for direct in directory:
        try:
            os.makedirs(direct)
        except FileExistsError:
            logger.warning(f'Каталог "{direct}" - уже существует')
        except PermissionError:
            logger.error(f'Каталог "{direct}" - недостаточно прав')
        except Exception as ex:
            logger.error(f'Каталог "{direct}" - ошибка: {ex}')


def remove(path_dir: str):
    """Удаление каталога. В случае если каталог полный, то путем удаления всех файлов

    Args:
          path_dir: полный путь до каталога
    """
    if os.path.exists(path_dir):
        for file_tmp in [f'{path_dir}/{one}' for one in os.listdir(path_dir)]:
            file.remove(file_tmp)

        try:
            os.rmdir(path_dir)
        except OSError:
            logger.error(f'Каталог "{path_dir}" - не возможно удалить! Его содержимое: {os.listdir(path_dir)}')
        else:
            logger.trace(f'Каталог "{path_dir}" - удален!')
    else:
        logger.warning(f'Каталог "{path_dir}" - не найден!')
