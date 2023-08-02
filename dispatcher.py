import telebot

from src.core.config import settings
from src.core.message import Message
from src.db.db import DatabaseSQLite


class CustomBot(telebot.TeleBot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = Message()
        self.db = DatabaseSQLite()


bot = CustomBot(token=settings.env.token, use_class_middlewares=True)
