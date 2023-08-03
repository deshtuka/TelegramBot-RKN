import telebot
from telebot.storage import StateRedisStorage

from src.core.config import settings
from src.core.message import Message
from src.db.db import DatabaseSQLite


class CustomBot(telebot.TeleBot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = Message()
        self.db = DatabaseSQLite()


bot = CustomBot(token=settings.env.token,
                use_class_middlewares=True,
                state_storage=StateRedisStorage(host=settings.env.redis_host, port=settings.env.redis_port))
