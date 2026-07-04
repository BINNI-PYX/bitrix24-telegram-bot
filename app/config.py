import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "bitrix24_bot")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "bitrix_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")

    BITRIX24_DOCS_URL = os.getenv(
        "BITRIX24_DOCS_URL",
        "https://apidocs.bitrix24.ru/"
    )

    YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
    YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
    YANDEX_MODEL = os.getenv("YANDEX_MODEL", "yandexgpt")

    DATABASE_URL = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()
