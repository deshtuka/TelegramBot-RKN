""" Модуль содержит регистрацию обработчиков """
from bot import bot
from . import bot_start as start
from . import bot_settings as settings
from . import bot_about as about


# Start
bot.register_message_handler(start.command_start, commands=['start'])
bot.register_message_handler(start.handler_captcha, content_types=['text'], regexp=r'^\d{2,4}$')
bot.register_callback_query_handler(start.button_create_report,
                                    func=lambda call: call.data and call.data == 'report_crt')
bot.register_callback_query_handler(start.handler_create_report,
                                    func=lambda call: call.data and call.data.startswith('date_'))
bot.register_callback_query_handler(start.button_get_report,
                                    func=lambda call: call.data and call.data == 'report_get')
bot.register_callback_query_handler(start.handler_download_report,
                                    func=lambda call: call.data and call.data.startswith('rsp_'))

# Settings
bot.register_message_handler(settings.command_settings, commands=['settings'])
bot.register_callback_query_handler(settings.button_setup_account,
                                    func=lambda call: call.data and call.data == 'settings_edit')
bot.register_callback_query_handler(settings.handler_del_account,
                                    func=lambda call: call.data and call.data == 'settings_delete')
bot.register_callback_query_handler(settings.handler_cancel_settings,
                                    func=lambda call: call.data and call.data == 'settings_cancel')
bot.register_message_handler(settings.handler_login_from_message, regexp=r'(?i)^(login=)')
bot.register_message_handler(settings.handler_password_from_message, regexp=r'(?i)^(password=)')

# About
bot.register_message_handler(about.command_about, commands=['about'])
