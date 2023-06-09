# -*- coding: utf-8 -*-
"""
Модуль функций проверок для обработчиков
"""
from bot import bot, BotDatabase

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def check_user_exists_in_database(chat_id):
    """Проверка наличия пользователя в базе данных

    Args:
        chat_id: идентификатор чата пользователя с ботом
    """

    if BotDatabase.check_chat_id(chat_id=chat_id) and BotDatabase.check_login_password(chat_id=chat_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton(bot.msg.CREATE_REPORT, callback_data='report_crt'),
            InlineKeyboardButton(bot.msg.GET_REPORT, callback_data='report_get')
        )

        bot.send_message(chat_id=chat_id, text=bot.msg.SELECT_ACTION, reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chat_id, text=bot.msg.INFO_SETTING)
