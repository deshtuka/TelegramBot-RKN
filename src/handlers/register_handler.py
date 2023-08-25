""" Модуль содержит регистрацию обработчиков """
from bot import bot
from . import start
from . import settings
from . import about
from . import feedback


# Start
bot.register_message_handler(start.command_start, commands=['start'])
bot.register_message_handler(start.handler_captcha, content_types=['text'], regexp=r'^\d{1,4}$')
bot.register_callback_query_handler(start.button_create_report,
                                    func=lambda call: call.data and call.data == 'btn_crt')
bot.register_callback_query_handler(start.handler_create_report,
                                    func=lambda call: call.data and call.data.startswith('btn_crt_on_'))
bot.register_callback_query_handler(start.button_get_report,
                                    func=lambda call: call.data and call.data == 'btn_get')
bot.register_callback_query_handler(start.handler_download_report,
                                    func=lambda call: call.data and call.data.startswith('btn_get_on_'))

# Settings
bot.register_message_handler(settings.command_settings, commands=['settings'])

# About
bot.register_message_handler(about.command_about, commands=['about'])

# Feedback
bot.register_message_handler(feedback.command_feedback, commands=['feedback'])
