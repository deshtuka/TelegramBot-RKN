FROM python:3.9

# запрет на буферизацию stdout и stderr
ENV PYTHONUNBUFFERED=1
# Не будет писать файлы .pyc (чтобы избежать проблем с обновлением кода в контейнере)
ENV PYTHONDONTWRITEBYTECODE=1

# Установить рабочую директорию в контейнере
WORKDIR /usr/src/app/rkn_bot

# Скопировать конфиг и установить виртуальное окружение
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать остальные файлы в контейнер
COPY . .
