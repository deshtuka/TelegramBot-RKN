"""
Модуль содержит обработчик команды /about
"""
from bot import bot


def command_about(message):
    """ Обработчик команды - about"""
    bot.send_message(message.chat.id, bot.msg.ABOUT)
