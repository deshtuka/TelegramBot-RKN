# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
import handlers

from config.public_keys import settings
from config.bot_message import Message
from utils import folders, db, logger, middleware
from dispatcher import bot

BotDatabase = db.BotDatabase(settings.file.database)

if __name__ == '__main__':
    folders.create(path_dirs=settings.dir.dict())
    BotDatabase.create_table_db()
    bot.setup_middleware(middleware.CustomMiddleware())
    bot.msg = Message()

    bot.polling(none_stop=True)
