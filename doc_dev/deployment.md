# Инструкция по разворачиванию проекта


### Скачать проект

Команда для скачивания проекта:
```bush
https://github.com/deshtuka/TelegramBot-RKN.git
```

### Добавить закрытые креды "secret_keys.env"

1) Создать файл "secret_keys.env" в корне проекта
```bush
touch /secret_keys.env
```

2) Добавить данные. Пример наполнения файла:
```dotenv
TOKEN_BOT="0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHER_KEY="0123456789"
```

### Создать пустой файл БД в локальной папке

#### Linux

1) В локальном хранилище создать пустой файл с разрешением `.db`
Пример:
```bush
mkdir -p /usr/src/app/database
touch /usr/src/app/database/database.db
```
2) Исправить путь в `volumes` файла `docker-compose.yml` на файл созданный в шаге 1.

#### Windows
1) В локальном хранилище создать пустой файл с разрешением `.db`
2) Исправить путь в `volumes` файла `docker-compose.yml` на файл созданный в шаге 1.

### Запустить docker-compose
```bush
docker-compose up -d --build
```

### Обновление 
```bush
docker-compose up -d --no-deps --build rkn_bot
```

### Остановить конвейер
```bush
docker-compose down
```


### Обновления проекта

Команда для обновления ветки:
```bush
cd ../usr/src/app/TelegramBot-RKN/
git fetch
git rebase origin/main
```

В случае локальных конфликтов:
```bush
git reset --hard origin/main
```
