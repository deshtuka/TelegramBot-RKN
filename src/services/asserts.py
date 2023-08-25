# -*- coding: utf-8 -*-
"""
Модуль функций проверок для обработчиков
"""
import datetime

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot
from src.core.config import settings


def check_user_exists_in_database(chat_id: id):
    """Проверка наличия пользователя в базе данных

    Args:
        chat_id: идентификатор чата пользователя с ботом
    """

    if bot.db.check_chat_id(chat_id=chat_id) and bot.db.check_login_password(chat_id=chat_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton(bot.msg.CREATE_REPORT, callback_data='btn_crt'),
            InlineKeyboardButton(bot.msg.GET_REPORT, callback_data='btn_get')
        )

        bot.send_message(chat_id=chat_id, text=bot.msg.SELECT_ACTION, reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chat_id, text=bot.msg.INFO_SETTING)


def is_cookie_active_less_than_25_min(chat_id: int) -> bool:
    """Проверка сохраненных данных сессии по активности.
    Если у пользователя была успешная активность в течение 25 минут, авторизация на сайте не нужна

    Args:
        chat_id: идентификатор чата пользователя с ботом
    Returns:
        bool: True - менее 25 мин / False - более 25 мин
    """
    datetime_string = bot.db.get_last_action(chat_id=str(chat_id))

    if datetime_string is None or not isinstance(datetime_string, str):
        return False

    dt_bd = datetime.datetime.strptime(datetime_string, settings.const.sql_datetime_format)

    dt_now = datetime.datetime.now()
    diff = dt_now - dt_bd

    total_minutes = diff.total_seconds() / 60
    return total_minutes <= 25
