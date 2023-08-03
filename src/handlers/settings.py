# -*- coding: utf-8 -*-
"""
Модуль содержит обработчики для настройки учетной записи пользователя
"""
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot.handler_backends import State, StatesGroup

from bot import bot
from src.services import asserts
from src.utils.crypto import Cryptography


class SettingStates(StatesGroup):
    login = State()
    password = State()


def command_settings(message):
    """ Обработчик команды - settings """
    chat_id = message.chat.id
    command = bot.msg.BTN_EDIT if bot.db.check_chat_id(chat_id=chat_id) else bot.msg.BTN_CREATE

    firstname = message.json['chat'].get('first_name')
    lastname = message.json['chat'].get('last_name')
    username = message.json['chat'].get('username')

    bot.db.add_personal_data(chat_id=chat_id, firstname=firstname, lastname=lastname, link=username)
    bot.db.add_date_settings(chat_id=chat_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton(command), KeyboardButton(bot.msg.BTN_DEL), KeyboardButton(bot.msg.BTN_CANCEL))

    bot.send_message(chat_id=message.chat.id, text=bot.msg.INFO_ACCOUNT, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in [bot.msg.BTN_EDIT, bot.msg.BTN_CREATE])
def handler_setup_account(message):
    """ Обработчик начала настройки учетной записи """
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(bot.msg.BTN_CANCEL))

    bot.set_state(message.from_user.id, SettingStates.login, message.chat.id)

    bot.send_message(message.chat.id, bot.msg.INFO_LOGIN, reply_markup=markup)


@bot.message_handler(state=SettingStates.login)
def handler_login_from_message(message):
    """ State 1. Обработчик логина """
    chat_id, user_id = message.chat.id, message.from_user.id

    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(bot.msg.BTN_CANCEL))

    bot.send_message(chat_id, bot.msg.INFO_PASSWORD, reply_markup=markup)

    bot.set_state(user_id, SettingStates.password, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data['login'] = message.text


@bot.message_handler(state=SettingStates.password)
def handler_password_from_message(message):
    """ State 2. Обработчик пароля """
    chat_id, user_id = message.chat.id, message.from_user.id

    with bot.retrieve_data(user_id, chat_id) as data:
        password_encrypted = Cryptography().custom_encrypt(message=message.text)

        bot.db.edit_login_and_password(chat_id=chat_id, login=data['login'], password=password_encrypted)

        bot.send_message(chat_id, bot.msg.DATA_SAVE, reply_markup=ReplyKeyboardRemove())
    bot.delete_state(user_id, chat_id)


@bot.message_handler(func=lambda message: message.text == bot.msg.BTN_DEL)
def handler_del_account(message):
    """ Обработчик удаления аккаунта """
    chat_id = message.chat.id

    bot.db.delete_account(chat_id=chat_id)

    bot.send_message(chat_id=chat_id, text=bot.msg.DATA_DEL, reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state='*', func=lambda message: message.text == bot.msg.BTN_CANCEL)
def handler_cancel_settings(message):
    """ Обработчик отмены настройки аккаунта (FSM и Keyboard сброс) """
    chat_id = message.chat.id

    bot.send_message(chat_id=chat_id, text=bot.msg.INFO_CANCEL, reply_markup=ReplyKeyboardRemove())
    bot.delete_state(message.from_user.id, chat_id)

    asserts.check_user_exists_in_database(chat_id=chat_id)
