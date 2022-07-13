# game_dev_api

# Переменные окружения

```dotenv
DATABASE_URL_LOCAL=postgresql://some_user:some_pass@some_host:port/some_db
CONFIG_EMAIL_SMTP=someemailwithsmtp@somemail.ru
CONFIG_PASSWORD_SMTP=somePASSforSMTPmail
```

## Локальная инициализация проекта

```bash
pip install -r requirements.txt
python main.py
```

## Инициализация проекта с помощью docker-compose

### 
```bash
docker-compose build
```

## Локальный запуск тестов

```bash
pytest
```

## Миграции
Используется Alembic https://alembic.sqlalchemy.org/en/latest/

### Запуск миграций в БД
```bash
alembic upgrade head
```
### Для проведения миграции инициализации базы данных в ручную можно использовать SQL код в директории migrations/


Схема базы данных:
![Database](img/db.jpeg)


# Используемые средства для разработки:

###FastAPI, asyncpg, postreSQL, celery, redis, docker, docker-compose, alembic, pytest, 

