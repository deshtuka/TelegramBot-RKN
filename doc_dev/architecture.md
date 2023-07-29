# Архитектура проекта

```
├── src
│   ├── api                 # Методы работы с API
│   │   ├── requests.py     
│   │   └── __init__.py
│   ├── services            # Бизнес логика
│   │   ├── asserts.py
│   │   ├── steps.py
│   │   └── __init__.py
│   ├── middlewares         # Логирование обработчика
│   │   ├── middleware.py   
│   │   └── __init__.py
│   ├── db                  # Методы для работы с БД
│   │   ├── db.py   
│   │   └── __init__.py
│   ├── core                # Это база
│   │   ├── config.py       # Публичные ключи
│   │   ├── logger.py       # Логирование
│   │   ├── message.py      # Тексты сообщений и команды
│   │   └── __init__.py
│   ├── utils               # Универсальные методы
│   │   ├── crypto.py
│   │   ├── file.py
│   │   ├── folders.py
│   │   ├── functions.py
│   │   └── __init__.py
│   ├── handlers            # Обработчики бота
│   │   ├── register_handler.py
│   │   ├── about.py
│   │   ├── settings.py
│   │   ├── start.py
│   │   └── __init__.py
│   └── __init__.py 
├── database                # База данных
│   └── database.db
├── temp                    # Временные файлы
│   ├── captcha
│   └── report
├── doc_dev                 # Документация
├── log                     # Логи 
├── venv                    # Виртуальное окружение
├── .gitignore
├── secret_keys.env
├── bot.py
├── dispatcher.py
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── readme.md
└── requirements.txt
```
