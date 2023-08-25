"""Модуль содержит класс по логированию обработчиков"""

from telebot.handler_backends import BaseMiddleware
from telebot.types import Message, CallbackQuery

from src.core.logger import log_active_user
from src.api.analytics import analytics


class CustomMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.update_sensitive = True
        self.update_types = ['message', 'edited_message', 'callback_query']

    @staticmethod
    def user_msg(query):
        return f'[ID:{query.from_user.id}][NAME: {query.from_user.full_name}]'

    # Отправка сообщения
    def pre_process_message(self, message: Message, data):
        """ Перед обработкой сообщения"""
        log_active_user(f'{self.user_msg(message)} отправлено сообщение: "{message.text}"')

        # Аналитика
        if not str(message.text).isdigit():
            analytics.write_bot_message(message=message)

    def post_process_message(self, message: Message, data, exception):
        """ После обработки сообщения"""
        log_active_user(f'{self.user_msg(message)} сообщение: "{message.text}" - обработано')

    # Изменение сообщения
    def pre_process_edited_message(self, message: Message, data):
        """ Перед обработкой изменения сообщения"""
        log_active_user(f'{self.user_msg(message)} изменено сообщение: "{message.text}"')

    def post_process_edited_message(self, message: Message, data, exception):
        """ После обработки изменения сообщения"""
        log_active_user(f'{self.user_msg(message)} изменение сообщения: "{message.text}" - завершено')

    # Действия с кнопками
    def pre_process_callback_query(self, callback_query: CallbackQuery, data: dict):
        """ Перед обработкой клика кнопки """
        log_active_user(f'{self.user_msg(callback_query)} нажал кнопку "{callback_query.data}"')

        # Аналитика
        text = str(callback_query.data)
        text = text.split('_on')[0] + '_on' if '_on' in text else text
        analytics.write_bot_callback(callback_query, text=text)

    def post_process_callback_query(self, callback_query: CallbackQuery, data: dict, exception: str):
        """ После обработкой клика кнопки """
        log_active_user(
            f'{self.user_msg(callback_query)} обработка события "{callback_query.data}" - завершена')
