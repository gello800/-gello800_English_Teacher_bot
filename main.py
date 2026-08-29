"""
English Learning Telegram Bot
Точка входа: инициализация базы данных, регистрация хэндлеров, запуск polling.
"""
import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import init_db
from handlers.start import start_command, help_command
from handlers.dictionary import (
    add_word_command,
    my_words_command,
    delete_word_callback,
    add_word_text_handler,
    WAITING_FOR_WORD,
)
from handlers.quiz import (
    quiz_command,
    quiz_answer_callback,
)
from handlers.voice import (
    pronounce_command,
    voice_message_handler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "Не задан BOT_TOKEN. Скопируйте .env.example в .env и укажите токен бота."
        )

    init_db()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Базовые команды
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Личный словарь пользователя
    application.add_handler(CommandHandler("add", add_word_command))
    application.add_handler(CommandHandler("mywords", my_words_command))
    application.add_handler(CallbackQueryHandler(delete_word_callback, pattern=r"^delword:"))

    # Квиз на перевод слов
    application.add_handler(CommandHandler("quiz", quiz_command))
    application.add_handler(CallbackQueryHandler(quiz_answer_callback, pattern=r"^quiz:"))

    # Тренировка произношения (распознавание голосовых сообщений)
    application.add_handler(CommandHandler("pronounce", pronounce_command))
    application.add_handler(MessageHandler(filters.VOICE, voice_message_handler))

    # Текстовые сообщения без команды — используются для добавления слова после /add
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, add_word_text_handler)
    )

    logger.info("Бот запущен. Ожидание сообщений...")
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
