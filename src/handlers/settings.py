# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot, BotDatabase
from src.services import asserts
from src.utils.crypto import Cryptography


def command_settings(message):
    """ Обработчик команды - settings """
    chat_id = message.chat.id
    command = bot.msg.BTN_EDIT if BotDatabase.check_chat_id(chat_id=chat_id) else bot.msg.BTN_CREATE

    firstname = message.json['chat'].get('first_name')
    lastname = message.json['chat'].get('last_name')
    username = message.json['chat'].get('username')

    BotDatabase.add_personal_data(chat_id=chat_id, firstname=firstname, lastname=lastname, link=username)
    BotDatabase.add_date_settings(chat_id=chat_id)

    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(command, callback_data='settings_edit'),
        InlineKeyboardButton(bot.msg.BTN_DEL, callback_data='settings_delete'),
        InlineKeyboardButton(bot.msg.BTN_CANCEL, callback_data='settings_cancel'),
    )

    bot.send_message(chat_id=message.chat.id, text=bot.msg.INFO_ACCOUNT, reply_markup=keyboard)


def button_setup_account(callback_query):
    """ Вывод кнопок для настройки аккаунта """
    bot.answer_callback_query(callback_query.id)
    bot.send_message(chat_id=callback_query.message.chat.id, text=bot.msg.INFO_LOGIN)


def handler_login_from_message(message):
    """ Обработчик логина """
    chat_id = message.chat.id
    login = str(message.text).lower().replace('login=', '')

    BotDatabase.edit_login(chat_id=chat_id, login=login)

    bot.send_message(chat_id=chat_id, text=bot.msg.INFO_PASSWORD)


def handler_password_from_message(message):
    """ Обработчик пароля """
    chat_id = message.chat.id
    password = str(message.text).lower().replace('password=', '')

    password_encrypted = Cryptography().custom_encrypt(message=password)

    BotDatabase.edit_password(chat_id=chat_id, password=password_encrypted)

    bot.send_message(chat_id=chat_id, text=bot.msg.DATA_SAVE)


def handler_del_account(callback_query):
    """ Обработчик удаления аккаунта """
    chat_id = callback_query.message.chat.id

    BotDatabase.delete_account(chat_id=chat_id)

    bot.answer_callback_query(callback_query.id)    # Отжать кнопку

    bot.send_message(chat_id=chat_id, text=bot.msg.DATA_DEL)


def handler_cancel_settings(callback_query):
    """ Обработчик отмены настройки аккаунта """
    bot.answer_callback_query(callback_query.id)

    # Вывод кнопок как при клике/вводе команды "/start"
    asserts.check_user_exists_in_database(chat_id=callback_query.message.chat.id)
