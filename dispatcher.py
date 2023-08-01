import telebot

from src.core.config import settings


bot = telebot.TeleBot(settings.env.token, use_class_middlewares=True)
