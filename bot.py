# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
import handlers

from config.public_keys import FILE_DATABASE, DIRECTORY_CAPTCHA, DIRECTORY_ARCHIVE, DIRECTORY_DEBUG
from config.bot_message import Message
from utils import folders, db, logger, middleware
from dispatcher import bot

BotDatabase = db.BotDatabase(FILE_DATABASE)

if __name__ == '__main__':
    folders.create(path_dirs=[DIRECTORY_CAPTCHA, DIRECTORY_ARCHIVE, DIRECTORY_DEBUG])
    BotDatabase.create_table_db()
    bot.setup_middleware(middleware.CustomMiddleware())
    bot.msg = Message()

    bot.polling(none_stop=True)
