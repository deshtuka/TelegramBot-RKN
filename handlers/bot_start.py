# -*- coding: utf-8 -*-
"""
Файл для работы телеграмм бота
"""
from config.public_keys import DIRECTORY_ARCHIVE_TEMP
from steps import bot_steps, bot_asserts
from utils import folders
from bot import bot

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
import datetime


# Обработчик команды - start
@bot.message_handler(commands='start')
def start_command(message):
    chat_id = message.chat.id
    bot_asserts.check_user_exists_in_database(chat_id=chat_id)


@bot.message_handler(commands='lol')
def lol_command(message):
    chat_id = message.chat.id

    res = bot_asserts.is_cookie_active_less_than_25_min(chat_id=chat_id)
    bot.send_message(chat_id, f'Результат = {res}')


# Обработчик капчи. Ввод пользователем 2-4 цифр с картинки
@bot.message_handler(content_types=['text'], regexp=r'^\d{2,4}$')
def get_text_messages(message):
    """ Обработчик текстовых сообщений чата

    Args:
        message: данные чата
    """
    chat_id = message.chat.id

    is_auth, msg_auth = bot_steps.authorization(secret_code_status=int(message.text), chat_id=chat_id)
    if is_auth:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton(bot.msg.CREATE_REPORT, callback_data='report_crt'),
            InlineKeyboardButton(bot.msg.GET_REPORT, callback_data='report_get')
        )
        bot.send_message(chat_id, bot.msg.SUCCESS_AUTH, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, bot.msg.ERROR_WITH_MSG.format(msg_auth))


# Вывод кнопок. Доступные даты для отправки создания заявки
@bot.callback_query_handler(lambda call: call.data and call.data == 'report_crt')
def create(callback_query):
    chat_id = callback_query.message.chat.id
    is_session = bot_steps.is_check_cookie(chat_id=chat_id)[0]

    # Бот. Снять состояние загрузки у кнопки, после клика
    bot.answer_callback_query(callback_query.id)

    if is_session:
        # Формирование словаря дат
        date_dict = {f'past_{i}': (datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%d.%m.%Y') for i in
                     range(0, 11 + 1)}

        # Формирование списка объектов кнопок с датами выше
        btn_list = [InlineKeyboardButton(val, callback_data=f'date_{val}') for val in date_dict.values()]

        # Добавление кнопок, вывод на экран
        inline_date = InlineKeyboardMarkup(row_width=3)
        inline_date.add(*btn_list)
        bot.send_message(chat_id, bot.msg.SELECT_DATE, reply_markup=inline_date)
    else:
        bot_steps.bot_get_captcha(bot, chat_id=chat_id)


# Обработчик. Пользователь выбрал кнопку с датой (Пример: 12.02.2021) - отправить запрос создания заявки
@bot.callback_query_handler(lambda call: call.data and call.data.startswith('date_'))
def check_date_button(callback_query):
    date = callback_query.data[5:]  # Дата формата dd.mm.YYYY
    chat_id = callback_query.message.chat.id

    # POST-запрос создания заявки
    is_response = bot_steps.create_report_for_date(date=date, chat_id=chat_id)

    # Бот. Снять состояние загрузки у кнопки, после клика
    bot.answer_callback_query(callback_query.id)

    msg = bot.msg.REQUEST_SENT.format(date) if is_response else bot.msg.REQUEST_NOT_SENT
    bot.send_message(chat_id, text=msg)


# Вывод кнопок. Получение данных с отчетами и вывод кнопок для выбора отчета на скачивание
@bot.callback_query_handler(lambda call: call.data and call.data == 'report_get')
def get_report(callback_query):
    chat_id = callback_query.message.chat.id
    is_session = bot_steps.is_check_cookie(chat_id=chat_id)[0]

    # Бот. Снять состояние загрузки у кнопки, после клика
    bot.answer_callback_query(callback_query.id)

    if is_session:
        # GET-запрос на получение страницы Отчетов
        response_result = bot_steps.page_report(chat_id=chat_id)

        if isinstance(response_result, dict) and len(response_result) > 0:
            # Вывод в чат кнопок с отчетами
            inline_response = InlineKeyboardMarkup(row_width=1)
            list_buttons = list()
            for key, value in response_result.items():
                list_buttons.append(InlineKeyboardButton(value, callback_data=f'rsp_{key}'))
            inline_response.add(*list_buttons)

            bot.send_message(chat_id=chat_id, text=bot.msg.REPORT_STATUS, reply_markup=inline_response)
            return None
        bot.send_message(chat_id=chat_id, text=bot.msg.ERROR_AUTH)
    bot_steps.bot_get_captcha(bot, chat_id=chat_id)


# Обработчик. Скачивание выбранного отчета
@bot.callback_query_handler(lambda call: call.data and call.data.startswith('rsp_'))
def download_report_button(callback_query):
    chat_id = callback_query.message.chat.id
    link_id = callback_query.data.split('_')[-1]    # id отчета для подстановки в ссылку
    date_rep = callback_query.data.split('_')[2]    # дата получаемого отчета

    is_response, bot_msg, path_to_files = bot_steps.download_the_selected_report(chat_id=chat_id, archive_id=link_id)

    # Бот. Снять состояние загрузки у кнопки, после клика
    bot.answer_callback_query(callback_query.id)

    if is_response:
        # Выгрузка в чат файлов + текст из csv
        if len(path_to_files) == 2:
            media = [
                InputMediaDocument(open(path_to_files[0], 'rb')),
                InputMediaDocument(open(path_to_files[1], 'rb'), caption=f'{date_rep} {bot_msg}')
            ]

            bot.send_media_group(chat_id=chat_id, media=media)
        else:
            bot.send_message(chat_id=chat_id, text=bot.msg.ERROR_UPLOAD_FILE_WITH_MSG.format(bot_msg))

        # Удаление временной папки
        folders.remove(path_dir=DIRECTORY_ARCHIVE_TEMP.format(archive_id=link_id))
    else:
        bot.send_message(chat_id=chat_id, text=bot_msg)
