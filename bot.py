# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
import handlers

from config.public_keys import settings
from config.bot_message import Message, Commands
from utils import folders, db, logger
import middlewares
from dispatcher import bot
from telebot.types import BotCommand


BotDatabase = db.BotDatabase(settings.file.database)

if __name__ == '__main__':
    # SetUp
    folders.create(path_dirs=settings.dir.dict())
    BotDatabase.create_table_db()

    # Настройка бота
    bot.setup_middleware(middlewares.middleware.CustomMiddleware())
    bot.msg = Message()

    # Список первоначальных команд
    bot.delete_my_commands(scope=None, language_code=None)
    bot.set_my_commands(commands=[BotCommand(str(key), value) for key, value in Commands().dict().items()])

    # Запуск бота
    bot.polling(none_stop=True)
