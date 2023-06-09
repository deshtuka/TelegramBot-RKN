"""
Логирование всех действий
"""
import time
from loguru import logger
from config.public_keys import FILE_DEBUG


logger.add(FILE_DEBUG, format='{time} {level} {message}', level='TRACE',
           rotation='7 day', compression='zip')


def log_request_response(response, level='INFO'):
    """Логирование Запрос/Ответа"""
    log_request(request=response, level=level)
    log_response(response=response, level=level)


def log_request(request, level):
    """Логирование запроса"""
    request = request.history[0].request if len(request.history) > 0 else request.request
    msg = {
        'Тип запроса': request.method,
        'URL запроса': request.url,
        'Headers запроса': request.headers,
    }
    log_display(msg=msg, level=level)


def log_response(response, level):
    """Логирование ответа"""
    msg = {
        'Код статуса ответа': response.status_code,
        'Headers ответа': response.headers
    }
    log_display(msg=msg, level=level)


def log_display(msg: dict, level: str) -> ...:
    """Вывод лога запроса/ответа"""
    row = ''
    for key, value in msg.items():
        row += f'\n{key:<18}: {value}'

    logger.log(level, row)


def log_active_user(message):
    """Логирование действий пользователя"""
    logger.opt(colors=True).info(f'<light-blue>{message}</light-blue>')


def log_time(message):
    """Декоратор времени выполнения действия"""

    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f'{message} - отправлен')
            start_time = time.time()

            result = func(*args, **kwargs)

            end_time = time.time()
            logger.info(f'{message} - получен! Время выполнения: {end_time - start_time:0.3f}s')

            return result

        return wrapper

    return actual_decorator
