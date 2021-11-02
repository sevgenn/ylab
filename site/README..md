# Сайт кулинарных рецептов

Сайт написан с использованием Django

## Запуск проекта

В корне проекта:
#### Запуск сервера на http://127.0.0.1:8000
python manage.py runserver
#### Применение миграций
python manage.py migrate
#### Сборка статики
python manage.py collectstatic
#### Добавление данных в базу
python manage.py loaddata mainapp/fixtures/data_db.json

В базе уже предустановлен администратор:
admin: пароль admin
и пользователь с ограниченными правами:
user1: пароль 4esz5rdx
