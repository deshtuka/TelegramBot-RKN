# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
from telebot.types import BotCommand

from src import handlers
from src.core import logger
from src.middlewares.middleware import CustomMiddleware
from src.core.config import settings
from src.core.message import Commands
from src.utils import folders
from dispatcher import bot


def bot_start(_bot):
    try:
        # Startup
        _bot.db.connect(settings.file.database)
        _bot.db.create_table_db()

        _bot.polling(none_stop=True)
    finally:
        # Shutdown
        _bot.stop_polling()
        _bot.db.close()


def main():
    # SetUp
    folders.create(path_dirs=settings.dir.dict())

    # Настройка бота
    bot.setup_middleware(CustomMiddleware())
    bot.delete_my_commands(scope=None, language_code=None)
    bot.set_my_commands(commands=[BotCommand(str(key), value) for key, value in Commands().dict().items()])

    bot_start(bot)


if __name__ == '__main__':
    main()
