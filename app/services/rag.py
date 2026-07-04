from app.db.crud import search_documents
from app.db.database import SessionLocal


def clean_text(text):
    lines = text.splitlines()
    clean_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line not in clean_lines:
            clean_lines.append(line)

    return "\n".join(clean_lines)


def build_answer(question):
    db = SessionLocal()

    try:
        pages = search_documents(db, question, limit=1)

        if not pages:
            return (
                "Я пока не нашёл точный ответ в загруженной документации Bitrix24.\n"
                "Попробуйте переформулировать вопрос."
            )

        page = pages[0]
        content = clean_text(page.content)

        preview = content[:900]

        answer = f"По документации Bitrix24 найден раздел: {page.title}\n\n"
        answer += preview + "...\n\n"
        answer += f"Источник: {page.url}"

        return answer

    finally:
        db.close()
