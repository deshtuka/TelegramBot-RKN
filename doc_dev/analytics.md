# Аналитика

### Какие блоки существуют?

1) Взаимодействие с ботом
2) Взаимодействие с сервером РКН
3) Взаимодействие с базой данных
4) Общие характеристики


### Какие метрики нужны?

1) Общее кол-во пользователей
2) Рейтинг. Пользователь - кол-во обращений к боту
3) Кол-во кликов кнопок (/start, /...)
4) Рейтинг. Ссылка ркн - кол-во запросов


### Метрики

1) Взаимодействие с ботом:

| Метрика          | Описание                                  |
|------------------|-------------------------------------------|
| rkn_bot_command  | Текстовое сообщение (/start, /help, ...)  |
| rkn_bot_callback | Действие callback (btn_crt, btn_get, ...) |

2) Прочее (в разработке)

| Метрика     | Задача                        |
|-------------|-------------------------------|
| rkn_server_ | Взаимодействие с сервером РКН |
| rkn_db_     | Взаимодействие с базой данных |
| rkn_common_ | Общие характеристики          |
