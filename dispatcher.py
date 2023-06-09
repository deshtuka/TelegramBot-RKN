from config.public_keys import TOKEN

import telebot

bot = telebot.TeleBot(TOKEN, use_class_middlewares=True)
