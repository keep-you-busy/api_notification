# Notification project

Этот проект разработан с использованием Python, Django, PostgreSQL, Redis и Celery.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/keep-you-busy/api_notification.git
    ```

2. Создайте и активируйте виртуальную среду:

    ```bash
    python -m venv --имя среды--
    source --имя среды--/bin/activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

5. Создайте суперпользователя:

    ```bash
    python manage.py createsuperuser
    ```

## Настройка базы данных

1. Убедитесь, что у вас установлен PostgreSQL [https://www.postgresql.org/download/]:

2. Создайте базу данных (пример в example.env):

4. Примените миграции:

    ```bash
    сd notification_backend
    python manage.py makemigrations
    python manage.py migrate
    ```

## Настройка Redis

1. Убедитесь, что у вас установлен Redis [https://redis.io/docs/install/install-redis/].

2. Запустите Redis на порту 6379.

## Настройка Celery


1. Запустите Celery worker:

    ```bash
    celery -A notification_backend worker -l info
    ```

## Запуск сервера

```bash
python manage.py runserver
```

По адресу /docs/ открывается страница со Swagger UI, где описание разработанного API.