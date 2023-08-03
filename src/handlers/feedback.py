"""
Модуль содержит обработчик команды /feedback
"""
from bot import bot
from src.core.config import settings


def command_feedback(message):
    """ Обработчик команды - feedback"""
    msg = bot.reply_to(message, bot.msg.FEEDBACK)
    bot.register_next_step_handler(msg, process_feedback_step)


def process_feedback_step(message):
    """ Обработчик отзыва """
    try:
        chat_id = message.chat.id
        text = message.text
        firstname = message.json['chat'].get('first_name')
        lastname = message.json['chat'].get('last_name')
        username = message.json['chat'].get('username')
        user_data = f'{chat_id}:@{username}|{firstname} {lastname}'

        if text != '/cancel' and settings.env.chat_id_admin > 0:
            bot.reply_to(message, bot.msg.FEEDBACK_GOOD)
            bot.send_message(settings.env.chat_id_admin, bot.msg.FEEDBACK_FROM_USER_FOR_ADMIN.format(user_data, text))

        bot.clear_step_handler_by_chat_id(chat_id)
    except Exception as ex:
        bot.reply_to(message, 'oooops')
