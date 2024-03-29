"""
Модуль содержит класс по работы с запросами на ведение аналитики
"""
from datetime import datetime
from typing import List, Dict

import requests
from telebot.types import Message, CallbackQuery
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
import loguru

from src.core.config import settings


class Analytics:
    """Класс передачи метрик в VictoriaMetrics по протоколу InfluxDB"""

    @staticmethod
    def __connect() -> InfluxDBClient:
        return InfluxDBClient(host=settings.env.vm_host, port=settings.env.vm_port, timeout=30_000, retries=1)

    def __write(self, json_body: List[Dict]):
        """Метод записи данных в VictoriaMetrics по протоколу InfluxDB

        Args:
            json_body: список словарей с передаваемыми данными
        """
        try:
            self.__connect().write_points(json_body, time_precision="s")

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout,
                InfluxDBClientError, InfluxDBServerError) as ex:
            loguru.logger.error(f'Аналитика (запрос): {ex}')

        except Exception as ex:
            loguru.logger.error(f'Аналитика (прочее): {ex}')

    def write_bot_message(self, message: Message):
        json_body = [{
            "measurement": "rkn_bot_command",
            "tags": {
                "chat_id": message.chat.id,
                "user_id": message.from_user.id,
                "full_name": message.from_user.full_name,
                "link": message.json['chat'].get('username'),
                "text": message.text
            },
            "time": datetime.now(),
            "fields": {
                "value": 1
            }
        }]

        self.__write(json_body)

    def write_bot_callback(self, callback_query: CallbackQuery, text: str):
        json_body = [{
            "measurement": "rkn_bot_callback",
            "tags": {
                "chat_id": callback_query.message.chat.id,
                "user_id": callback_query.from_user.id,
                "full_name": callback_query.from_user.full_name,
                "link": callback_query.from_user.username,
                "text": text
            },
            "time": datetime.now(),
            "fields": {
                "value": 1
            }
        }]

        self.__write(json_body)

    def write_sql(self):
        ...

    def write_request(self):
        ...


analytics = Analytics()
