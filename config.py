"""
Конфигурация бота. Значения берутся из переменных окружения / файла .env
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Токен бота, полученный от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Путь к файлу базы данных SQLite
DB_PATH = os.getenv("DB_PATH", "bot_database.db")

# Язык распознавания речи (Google Speech Recognition)
SPEECH_LANGUAGE = os.getenv("SPEECH_LANGUAGE", "en-US")

# Минимальное количество слов в квизе, при котором квиз доступен
MIN_WORDS_FOR_QUIZ = 4
