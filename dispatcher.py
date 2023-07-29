from src.core.config import settings

import telebot

bot = telebot.TeleBot(settings.env.token, use_class_middlewares=True)
