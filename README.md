# backend

Асинхронное подключение к базе + SQLAlchemy 2 + Pydantic 2

[Source](https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable)

## Настройка окружения
1. Установка виртуального окружения и зависимостей
```shell
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

2. Засинхрониться с alembic(или создать новую, только обратить внимание на `alembic.init` и `alembic/env.py`)
```shell
alembic init -t async alembic
```

## Запуск проекта
1. Запускаем тестовый шаблон
```shell
uvicorn src.main:app --reload
```

2. Миграции в проекте
```shell
alembic revision --autogenerate -m "Create test base table"  
```

3. Применение миграции
```shell
alembic upgrade head
```

# Через Docker