# Образ основы контейнера
FROM python:3.8.10
ENV PYTHONUNBUFFERED 1
# Рабочая директория в проекте
WORKDIR /cookbook_root
# Установка зависимостей
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# Копирование папки в контейнер
COPY . .