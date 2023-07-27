"""
Модуль константных сообщений бота
"""
from pydantic import BaseModel


class Commands(BaseModel):
    """Класс команд с кратким описанием"""
    start:      str = 'Сформировать и получить отчет за необходимую дату'
    settings:   str = 'Настройка учетной записи'
    about:      str = 'Информация о сути данного проекта'
    feedback:   str = 'Оставить отзыв по работе бота'


class Message(BaseModel):
    """Класс сообщений которые выводит бот"""
    # Действия
    CREATE_REPORT:  str = 'Создать заявку 🐒'
    GET_REPORT:     str = 'Получить отчет'
    SELECT_DATE:    str = 'Шлепни дату:'

    BTN_EDIT:   str = 'Изменить'
    BTN_CREATE: str = 'Создать'
    BTN_DEL:    str = 'Удалить'
    BTN_CANCEL: str = 'Отмена'

    # Информационные
    SUCCESS_AUTH:   str = 'Сойдет! Твори грязь, но сделай выбор 😈'
    DATA_SAVE:      str = 'Ваши данные сохранены!'
    DATA_DEL:       str = 'Учетная запись успешно удалена из базы данных!\nВозвращайтесь!'
    SELECT_ACTION:  str = 'Выберите действие:'

    REPORT_STATUS:  str = 'Статус отчетов:'
    INFO_ACCOUNT:   str = 'Что нужно сделать с учетной записью?'
    INFO_LOGIN:     str = 'Для доступа к сервису РосКомНадзора необходимо ввести Ваши данные от учетной записи\n\n' \
                          'Введите логин с командой login:\nПример: login=admin'
    INFO_PASSWORD:  str = 'Отлично, теперь осталось ввести пароль с командой password\n\nПример: password=123'
    INFO_SETTING:   str = 'Необходимо настроить аккаунт!\nДля этого введите команду:\n/settings'

    COOKIES_GOOD:   str = 'Проверка активности куков: куки рабочие!'
    COOKIES_BAD:    str = 'Проверка активности куков: куки не рабочие!'

    # Предупреждения
    REQUEST_SENT:               str = 'Заявка на {} - Шлепнулась!'
    REQUEST_NOT_SENT:           str = 'Заявка на {} - НЕ ШЛЕПНУЛАСЬ!'
    ERROR_UPLOAD_FILE_WITH_MSG: str = 'Не возможно выгрузить все файлы!\n{}'
    ERROR_CAPTCHA:              str = 'Касяк, не могу получить капчу! Не работает сайт!'

    # Ошибки
    ERROR_WITH_MSG: str = 'Опаньки! {}'
    ERROR_AUTH:     str = 'Опаньки! Нужна авторизация'
    ERROR_DOWNLOAD: str = 'Архив не скачен'
