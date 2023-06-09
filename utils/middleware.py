"""Модуль содержит класс по логированию обработчиков"""

from telebot.handler_backends import BaseMiddleware
from telebot import types

from utils.logger import log_active_user


class CustomMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.update_sensitive = True
        self.update_types = ['message', 'edited_message', 'callback_query']

    @staticmethod
    def user_msg(query):
        return f'[ID:{query.from_user.id}][NAME: {query.from_user.full_name}]'

    # Отправка сообщения
    def pre_process_message(self, message, data):
        """ Перед обработкой сообщения"""
        log_active_user(f'{self.user_msg(message)} отправлено сообщение: "{message.text}"')

    def post_process_message(self, message, data, exception):
        """ После обработки сообщения"""
        log_active_user(f'{self.user_msg(message)} сообщение: "{message.text}" - обработано')

    # Изменение сообщения
    def pre_process_edited_message(self, message, data):
        """ Перед обработкой изменения сообщения"""
        log_active_user(f'{self.user_msg(message)} изменено сообщение: "{message.text}"')

    def post_process_edited_message(self, message, data, exception):
        """ После обработки изменения сообщения"""
        log_active_user(f'{self.user_msg(message)} изменение сообщения: "{message.text}" - завершено')

    # Действия с кнопками
    def pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        """ Перед обработкой клика кнопки """
        log_active_user(f'{self.user_msg(callback_query)} нажал кнопку "{callback_query.json["data"]}"')

    def post_process_callback_query(self, callback_query: types.CallbackQuery, data: dict, exception: str):
        """ После обработкой клика кнопки """
        log_active_user(
            f'{self.user_msg(callback_query)} обработка события "{callback_query.json["data"]}" - завершена')
