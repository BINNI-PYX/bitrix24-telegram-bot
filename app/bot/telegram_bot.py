from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from app.config import settings
from app.db.crud import get_or_create_user, save_message
from app.db.database import SessionLocal
from app.yandex_assistant.client import ask_assistant


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для ответов по документации Bitrix24 API. "
        "Напиши вопрос текстом."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    question = update.message.text

    db = SessionLocal()

    try:
        get_or_create_user(
            db=db,
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name
        )

        answer = ask_assistant(question)

        save_message(
            db=db,
            telegram_id=user.id,
            question=question,
            answer=answer
        )

        await update.message.reply_text(answer)

    finally:
        db.close()


def run_bot():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram bot started")
    app.run_polling()
