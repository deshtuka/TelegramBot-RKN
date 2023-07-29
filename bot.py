# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
from src import handlers
from src.core import logger
from src.db import db
from src.middlewares import middleware
from src.core.config import settings
from src.core.message import Message, Commands
from src.utils import folders
from dispatcher import bot
from telebot.types import BotCommand


BotDatabase = db.BotDatabase(settings.file.database)


def start(bot):
    # Запуск бота
    try:
        bot.polling(none_stop=True)
    finally:
        bot.stop_polling()


def main():
    # SetUp
    folders.create(path_dirs=settings.dir.dict())
    BotDatabase.create_table_db()

    # Настройка бота
    bot.setup_middleware(middleware.CustomMiddleware())
    bot.msg = Message()

    # Список первоначальных команд
    bot.delete_my_commands(scope=None, language_code=None)
    bot.set_my_commands(commands=[BotCommand(str(key), value) for key, value in Commands().dict().items()])

    start(bot)


if __name__ == '__main__':
    main()

