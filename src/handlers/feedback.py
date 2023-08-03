"""
Модуль содержит обработчик команды /feedback
"""
from telebot.handler_backends import State, StatesGroup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot import bot
from src.core.config import settings


class FeedbackStates(StatesGroup):
    message = State()


def command_feedback(message):
    """ Обработчик команды - feedback (FSM первоначальное состояние)"""
    chat_id = message.chat.id

    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

    bot.set_state(message.from_user.id, FeedbackStates.message, chat_id)

    bot.send_message(chat_id, bot.msg.FEEDBACK, reply_markup=markup)


@bot.message_handler(state='*', commands='cancel')
def handler_cancel_any_state(message):
    """ Обработчик команды - /cancel (FSM и Keyboard сброс)"""
    bot.send_message(message.chat.id, bot.msg.INFO_CANCEL, reply_markup=ReplyKeyboardRemove())
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=FeedbackStates.message)
def handler_feedback(message):
    """ Обработчик сообщения пользователя и отправка админу отзыва"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    firstname = message.json['chat'].get('first_name')
    lastname = message.json['chat'].get('last_name')
    username = message.json['chat'].get('username')
    user_data = f'{chat_id}:@{username}|{firstname} {lastname}'

    bot.send_message(chat_id, bot.msg.FEEDBACK_GOOD, reply_markup=ReplyKeyboardRemove())

    if settings.env.chat_id_admin > 0:
        bot.send_message(settings.env.chat_id_admin,
                         bot.msg.FEEDBACK_FROM_USER_FOR_ADMIN.format(user_data, message.text))

    bot.delete_state(user_id, chat_id)
