# Bitrix24 RAG Telegram Bot

Телеграм-бот для поиска информации по официальной документации Bitrix24 REST API.

## Возможности

- поиск информации по документации Bitrix24;
- работа через Telegram;
- хранение пользователей и истории сообщений;
- использование PostgreSQL;
- использование SQLAlchemy ORM;
- парсинг документации через Requests, BeautifulSoup и Selenium;
- локальный RAG-поиск по сохранённой документации.

## Структура проекта

app/
- bot/ — модуль Telegram-бота;
- db/ — модели базы данных и CRUD-операции;
- docs_parser/ — парсер документации Bitrix24;
- services/ — сервисы проекта и RAG-поиск;
- yandex_assistant/ — модуль интеграции с Yandex Assistant;
- config.py — настройки проекта;
- init_db.py — создание таблиц базы данных;
- main.py — запуск приложения.

## Используемые технологии

- Python 3
- PostgreSQL
- SQLAlchemy
- Requests
- BeautifulSoup
- Selenium
- python-telegram-bot
- python-dotenv

## Настройка проекта

Создать виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Заполнить файл `.env`:

```text
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=bitrix24_bot
POSTGRES_USER=bitrix_user
POSTGRES_PASSWORD=12345

BITRIX24_DOCS_URL=https://apidocs.bitrix24.ru/
```

## Создание базы данных

Создать таблицы:

```bash
python -m app.init_db
```

## Загрузка документации

Загрузить страницы документации Bitrix24:

```bash
python -m app.docs_parser.crawler
```

Проверить Selenium-парсер:

```bash
python -m app.docs_parser.selenium_parser
```

## Проверка поиска

Проверить работу RAG-поиска:

```bash
python -m app.test_rag
```

## Запуск Telegram-бота

```bash
python -m app.main
```

## Источник документации

https://apidocs.bitrix24.ru/
