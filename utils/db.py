# -*- coding: utf-8 -*-
"""
Класс с методами для работы с базой данных
"""
import sqlite3


class BotDatabase:

    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table_db(self):
        """Создание двух таблиц БД. Первая (config) с конфигурациями, вторая (users) с данными о пользователе"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS config(
                chat_id INT PRIMARY KEY UNIQUE NOT NULL,
                login TEXT,
                password TEXT,
                user_agent TEXT,
                secret_code_id INT,
                cookies TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                chat_id INT UNIQUE NOT NULL,
                firstname TEXT,
                lastname TEXT,
                link TEXT,
                FOREIGN KEY (chat_id) REFERENCES CONFIG(chat_id));
        """)
        return self.conn.commit()

    # Проверки
    def check_chat_id(self, chat_id):
        """Проверка, существует ли пользователь в таблице"""
        result = self.cursor.execute("SELECT * FROM config WHERE chat_id=?;", (str(chat_id), ))
        return bool(len(result.fetchall()))

    def check_login_password(self, chat_id):
        """Проверка, настроенна ли учетная запись (обязательно логин и пароль указан)"""
        result = self.cursor.execute("SELECT login, password FROM config WHERE chat_id=?;", (str(chat_id), ))
        return all(result.fetchall()[0])

    # Настройки
    def edit_login(self, chat_id, login):
        """Изменить логин учетной записи"""
        self.cursor.execute("UPDATE config SET login=? WHERE chat_id=?;", (login, str(chat_id)))
        return self.conn.commit()

    def edit_password(self, chat_id, password):
        """Изменить пароль учетной записи"""
        self.cursor.execute("UPDATE config SET password=? WHERE chat_id=?;", (password, str(chat_id)))
        return self.conn.commit()

    def delete_account(self, chat_id):
        """Удаление данных конфигураций аккаунта из БД"""
        self.cursor.execute("DELETE FROM config WHERE chat_id=?;", (str(chat_id), ))
        return self.conn.commit()

    def add_personal_data(self, chat_id, firstname, lastname, link):
        """Добавление персональных данных пользователя для логирования"""
        self.cursor.execute("INSERT or IGNORE INTO config (chat_id) VALUES (?);", (str(chat_id), ))
        self.cursor.execute(
            "INSERT or IGNORE INTO users (chat_id, firstname, lastname, link) VALUES (?, ?, ?, ?);",
            (str(chat_id), firstname, lastname, link)
        )
        return self.conn.commit()

    # Получение данных
    def get_login_password(self, chat_id):
        """Получить логин и пароль учетной записи"""
        if self.check_chat_id(chat_id=chat_id):
            result = self.cursor.execute("SELECT login, password FROM config WHERE chat_id=?;", (str(chat_id), ))
            return result.fetchone()

    def get_username(self, chat_id):
        """Получить короткую ссылку пользователя для логирования"""
        if self.check_chat_id(chat_id=chat_id):
            result = self.cursor.execute("""
                SELECT firstname, lastname FROM users 
                LEFT JOIN config ON users.chat_id = config.chat_id 
                WHERE config.chat_id=?;
            """, (str(chat_id), ))
            return result.fetchone()

    def get_user_agent(self, chat_id):
        """Получить user-agent пользователя"""
        result = self.cursor.execute("SELECT user_agent FROM config WHERE chat_id=?;", (str(chat_id), ))
        result = result.fetchone()[0]
        return eval(result) if isinstance(result, str) else None

    def get_secret_code_id(self, chat_id):
        """Получить secretcodeId пользователя"""
        result = self.cursor.execute("SELECT secret_code_id FROM config WHERE chat_id=?;", (str(chat_id), ))
        return result.fetchone()[0]

    def get_cookies(self, chat_id):
        """Получить cookies пользователя"""
        result = self.cursor.execute("SELECT cookies FROM config WHERE chat_id=?;", (str(chat_id), ))
        result = result.fetchone()[0]
        return eval(result) if isinstance(result, str) else None

    # Изменений данных
    def edit_user_agent(self, chat_id, user_agent):
        """Изменить запись user-agent"""
        self.cursor.execute("UPDATE config SET user_agent=? WHERE chat_id=?;", (user_agent, str(chat_id)))
        return self.conn.commit()

    def edit_secret_code_id(self, chat_id, secret_code_id: int):
        """Изменить запись secretcodeId"""
        self.cursor.execute("UPDATE config SET secret_code_id=? WHERE chat_id=?;", (secret_code_id, str(chat_id)))
        return self.conn.commit()

    def edit_cookies(self, chat_id, cookies):
        """Изменить запись cookies"""
        self.cursor.execute("UPDATE config SET cookies=? WHERE chat_id=?;", (cookies, str(chat_id)))
        return self.conn.commit()

    def close(self):
        """Закрыть соединение с БД"""
        self.conn.close()
