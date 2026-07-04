from app.db.crud import get_or_create_user, save_message
from app.db.database import SessionLocal


db = SessionLocal()

user = get_or_create_user(
    db=db,
    telegram_id=123456,
    username="test_user",
    first_name="Test"
)

message = save_message(
    db=db,
    telegram_id=123456,
    question="Что такое Bitrix24 API?",
    answer="Тестовый ответ"
)

print("Пользователь:", user.id, user.telegram_id)
print("Сообщение:", message.id, message.question)

db.close()
