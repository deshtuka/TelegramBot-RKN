# -*- coding: utf-8 -*-
"""
Класс с методами для работы с базой данных
"""
import sqlite3
from loguru import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseSQLite(metaclass=Singleton):
    """Класс работы с БД SQLite"""

    def __init__(self):
        self.conn = None
        self.cursor = None

        if self.conn is None and self.cursor is None:
            logger.warning('БД - нужно подключение')

    def connect(self, db_file):
        """Подключение к БД"""
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.conn.set_trace_callback(logger.info)
        except sqlite3.Error as ex:
            logger.error(f'БД - ошибка подключения: {ex}')
        else:
            logger.success('БД - связь установлена')

    def create_table_db(self):
        """Создание двух таблиц БД. Первая (config) с конфигурациями, вторая (users) с данными о пользователе"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS config(
                chat_id INT PRIMARY KEY UNIQUE NOT NULL,
                login TEXT,
                password TEXT,
                user_agent TEXT,
                secret_code_id INT,
                cookies TEXT,
                last_action DATETIME
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                chat_id INT UNIQUE NOT NULL,
                firstname TEXT,
                lastname TEXT,
                link TEXT,
                date_add DATETIME,
                FOREIGN KEY (chat_id) REFERENCES CONFIG(chat_id));
        """)
        return self.conn.commit()

    # Проверки
    def check_chat_id(self, chat_id: str):
        """Проверка, существует ли пользователь в таблице"""
        result = self.cursor.execute("SELECT * FROM config WHERE chat_id=?;", (chat_id, ))
        return bool(len(result.fetchall()))

    def check_login_password(self, chat_id: str):
        """Проверка, настроена ли учетная запись (обязательно логин и пароль указан)"""
        result = self.cursor.execute("SELECT login, password FROM config WHERE chat_id=?;", (chat_id, ))
        return all(result.fetchall()[0])

    # Настройки
    def edit_login(self, chat_id: str, login):
        """Изменить логин учетной записи"""
        self.cursor.execute("UPDATE config SET login=? WHERE chat_id=?;", (login, chat_id))
        return self.conn.commit()

    def edit_password(self, chat_id: str, password):
        """Изменить пароль учетной записи"""
        self.cursor.execute("UPDATE config SET password=? WHERE chat_id=?;", (password, chat_id))
        return self.conn.commit()

    def delete_account(self, chat_id: str):
        """Удаление данных конфигураций аккаунта из БД"""
        self.cursor.execute("DELETE FROM config WHERE chat_id=?;", (chat_id, ))
        return self.conn.commit()

    def add_personal_data(self, chat_id: str, firstname, lastname, link):
        """Добавление персональных данных пользователя"""
        self.cursor.execute("INSERT or IGNORE INTO config (chat_id) VALUES (?);", (chat_id, ))
        self.cursor.execute(
            "INSERT or IGNORE INTO users (chat_id, firstname, lastname, link) VALUES (?, ?, ?, ?);",
            (str(chat_id), firstname, lastname, link)
        )
        return self.conn.commit()

    def add_date_settings(self, chat_id: str):
        self.cursor.execute("UPDATE users SET date_add=datetime('now', 'localtime') WHERE chat_id=?;", (chat_id, ))
        return self.conn.commit()

    # Получение данных
    def get_login_password(self, chat_id: str):
        """Получить логин и пароль учетной записи"""
        if self.check_chat_id(chat_id=chat_id):
            result = self.cursor.execute("SELECT login, password FROM config WHERE chat_id=?;", (chat_id, ))
            return result.fetchone()

    def get_session(self, chat_id: str):
        """Получение данных для авторизации: user-agent, secretcodeId, cookies"""
        result = self.cursor.execute(
            "SELECT user_agent, secret_code_id, cookies FROM config WHERE chat_id=?;", (chat_id,)
        )
        data = result.fetchone()
        return (
            eval(data[0]) if isinstance(data[0], str) else None,    # user_agent
            data[1],                                                # secret_code_id
            eval(data[2]) if isinstance(data[2], str) else None     # cookies
        )

    def get_last_action(self, chat_id: str):
        """Получить дату и время последней активности куков"""
        result = self.cursor.execute("SELECT last_action FROM config WHERE chat_id=?;", (chat_id,))
        return result.fetchone()[0]

    def add_last_action(self, chat_id: str):
        self.cursor.execute("UPDATE config SET last_action=datetime('now', 'localtime') WHERE chat_id=?;", (chat_id, ))
        return self.conn.commit()

    # Изменений данных
    def edit_session(self, chat_id: str, user_agent, secret_code_id: int, cookies):
        """Изменить запись авторизации: user-agent, secretcodeId, cookies"""
        self.cursor.execute("UPDATE config SET user_agent=?, secret_code_id=?, cookies=? WHERE chat_id=?;",
                            (user_agent, secret_code_id, cookies, chat_id))
        return self.conn.commit()

    def close(self):
        """Закрыть соединение с БД"""
        if self.conn:
            self.conn.close()
            logger.success('БД - связь разорвана')
        else:
            logger.warning('БД - нет активного подключения')

