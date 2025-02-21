# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем необходимые зависимости для системы
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей requirements.txt
COPY requirements.txt /app/

# Устанавливаем зависимости проекта через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# Указываем команду для запуска проекта
CMD ["python3.12", "-m", "project1"]
