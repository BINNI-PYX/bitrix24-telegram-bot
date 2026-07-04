import requests

from app.config import settings
from app.db.crud import search_documents
from app.db.database import SessionLocal
from app.services.rag import build_answer


YANDEX_COMPLETION_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


def get_context_from_database(question):
    db = SessionLocal()

    try:
        pages = search_documents(db, question, limit=2)

        if not pages:
            return ""

        context_parts = []

        for page in pages:
            context_parts.append(
                f"Источник: {page.title}\n"
                f"Ссылка: {page.url}\n"
                f"Текст:\n{page.content[:2500]}"
            )

        return "\n\n---\n\n".join(context_parts)

    finally:
        db.close()


def ask_yandex_gpt(question, context):
    headers = {
        "Authorization": f"Api-Key {settings.YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"gpt://{settings.YANDEX_FOLDER_ID}/{settings.YANDEX_MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": 1200
        },
        "messages": [
            {
                "role": "system",
                "text": (
                    "Ты помощник для разработчиков Bitrix24 REST API. "
                    "Отвечай кратко, точно и только на основе переданного контекста. "
                    "Если ответа в контексте нет, скажи, что информации недостаточно."
                )
            },
            {
                "role": "user",
                "text": (
                    f"Вопрос пользователя:\n{question}\n\n"
                    f"Контекст из документации Bitrix24:\n{context}"
                )
            }
        ]
    }

    response = requests.post(
    YANDEX_COMPLETION_URL,
    headers=headers,
    json=data,
    timeout=60
    )

    response.raise_for_status()
    result = response.json()

    return result["result"]["alternatives"][0]["message"]["text"]


def ask_assistant(question):
    context = get_context_from_database(question)

    if not settings.YANDEX_API_KEY or not settings.YANDEX_FOLDER_ID:
        return build_answer(question)

    if not context:
        return (
            "Я пока не нашёл подходящую информацию в базе знаний Bitrix24. "
            "Попробуйте переформулировать вопрос."
        )

    try:
        answer = ask_yandex_gpt(question, context)
        return answer

    except Exception as error:
        print("YANDEX ERROR:")
        print(error)
        raise


def update_knowledge_base():
    from app.docs_parser.crawler import crawl_main_links

    crawl_main_links()
