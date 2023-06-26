# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
from bot import bot, BotDatabase
from steps import bot_asserts
from utils.crypto import Cryptography

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


# Обработчик команды - settings
@bot.message_handler(commands='settings')
def settings_command(message):
    chat_id = message.chat.id
    # Проверка существования пользователя в Базе данных для вывода соответствующей команды
    command = bot.msg.BTN_EDIT if BotDatabase.check_chat_id(chat_id=chat_id) else bot.msg.BTN_CREATE

    # Данные о пользователе
    firstname = message.json['chat'].get('first_name')
    lastname = message.json['chat'].get('last_name')
    username = message.json['chat'].get('username')

    # Добавление информации о пользователе в БД для логирования его действий
    BotDatabase.add_personal_data(chat_id=chat_id, firstname=firstname, lastname=lastname, link=username)
    BotDatabase.add_date_settings(chat_id=chat_id)

    # Вывод кнопок
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(command, callback_data='settings_edit'),
        InlineKeyboardButton(bot.msg.BTN_DEL, callback_data='settings_delete'),
        InlineKeyboardButton(bot.msg.BTN_CANCEL, callback_data='settings_cancel'),
    )

    bot.send_message(chat_id=message.chat.id, text=bot.msg.INFO_ACCOUNT, reply_markup=keyboard)


# Вывод действий для настройки аккаунта
@bot.callback_query_handler(lambda call: call.data and call.data == 'settings_edit')
def setup_account(callback_query):
    chat_id = callback_query.message.chat.id

    # Бот. Снять состояние загрузки у кнопки, после клика
    bot.answer_callback_query(callback_query.id)

    bot.send_message(chat_id=chat_id, text=bot.msg.INFO_LOGIN)


# Обработчик логина.
@bot.message_handler(regexp=r'^(login=)')
def get_login_from_message(message):
    chat_id = message.chat.id
    text_input = str(message.text)
    login = text_input.replace('login=', '')

    # Добавление в БД Логина
    BotDatabase.edit_login(chat_id=chat_id, login=login)

    bot.send_message(chat_id=chat_id, text=bot.msg.INFO_PASSWORD)


# Обработчик пароля.
@bot.message_handler(regexp=r'^(password=)')
def get_password_from_message(message):
    chat_id = message.chat.id
    text_input = str(message.text)
    password = text_input.replace('password=', '')

    # Зашифровка пароля
    password_encrypted = Cryptography().custom_encrypt(message=password)

    # Добавление в БД Пароля
    BotDatabase.edit_password(chat_id=chat_id, password=password_encrypted)

    bot.send_message(chat_id=chat_id, text=bot.msg.DATA_SAVE)


# Удаление аккаунта
@bot.callback_query_handler(lambda call: call.data and call.data == 'settings_delete')
def del_account(callback_query):
    chat_id = callback_query.message.chat.id

    # Бот. Снять состояние загрузки у кнопки, после клика
    bot.answer_callback_query(callback_query.id)

    # Удаление из БД всех данных
    BotDatabase.delete_account(chat_id=chat_id)

    bot.send_message(chat_id=chat_id, text=bot.msg.DATA_DEL)


# Отмена настройки аккаунта
@bot.callback_query_handler(lambda call: call.data and call.data == 'settings_cancel')
def user_cancel(callback_query):
    chat_id = callback_query.message.chat.id

    # Бот. Снять состояние загрузки у кнопки, после клика
    bot.answer_callback_query(callback_query.id)

    # Вывод кнопок как при клике/вводе команды "/start"
    bot_asserts.check_user_exists_in_database(chat_id=chat_id)
