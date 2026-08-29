# 🇬🇧 English Learning Telegram Bot

Telegram-бот для изучения английского языка: личный словарь, квизы на перевод
и **тренировка произношения с распознаванием голосовых сообщений**.

## Возможности

- `/start`, `/help` — приветствие и список команд
- `/add` — добавить слово в личный словарь (`word - перевод`)
- `/mywords` — посмотреть свой словарь, удалить слова
- `/quiz` — квиз с вариантами ответа на перевод слова
- `/pronounce` — бот даёт слово, ты произносишь его голосовым сообщением,
  бот распознаёт речь (Google Speech Recognition) и сравнивает с ожидаемым
  словом
- Любое голосовое сообщение вне тренировки — бот просто присылает текст
  распознанной речи

## Стек

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v21 (async)
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) + Google Web Speech API (бесплатно, без ключа)
- [pydub](https://github.com/jiaaro/pydub) для конвертации `.ogg` → `.wav`
- SQLite для хранения пользователей и словарей

## Установка

### 1. Системные зависимости

Для конвертации голосовых сообщений нужен **ffmpeg**:

```bash
# Ubuntu / Debian
sudo apt-get update && sudo apt-get install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

### 2. Клонирование и виртуальное окружение

```bash
git clone <URL_вашего_репозитория>
cd telegram_english_bot
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Настройка токена

1. Получите токен у [@BotFather](https://t.me/BotFather) в Telegram.
2. Скопируйте `.env.example` в `.env` и вставьте токен:

```bash
cp .env.example .env
```

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### 4. Запуск

```bash
python main.py
```

## Запуск через Docker

```bash
docker build -t english-bot .
docker run -d --name english-bot --env-file .env english-bot
```

Образ уже содержит `ffmpeg`, отдельно ставить не нужно.

## Структура проекта

```
telegram_english_bot/
├── main.py                # точка входа, регистрация хэндлеров
├── config.py               # чтение переменных окружения
├── database.py              # работа с SQLite
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── handlers/
│   ├── start.py            # /start, /help
│   ├── dictionary.py       # /add, /mywords
│   ├── quiz.py              # /quiz
│   └── voice.py             # /pronounce + обработка голосовых
└── utils/
    ├── speech.py            # распознавание речи (ogg -> wav -> текст)
    └── words_data.py        # встроенный набор слов
```

## Как работает распознавание голоса

1. Пользователь отправляет голосовое сообщение (Telegram формат `.ogg/OPUS`).
2. Бот скачивает файл через `Bot.get_file`.
3. `pydub` конвертирует `.ogg` в `.wav` (нужен ffmpeg).
4. `SpeechRecognition` отправляет `.wav` в Google Web Speech API и получает текст.
5. В режиме `/pronounce` распознанный текст сравнивается с ожидаемым словом
   через `difflib.SequenceMatcher`; при совпадении ≥ 80% слово засчитывается
   выученным.

> Google Web Speech API в библиотеке SpeechRecognition бесплатен и не требует
> ключа, но имеет неофициальные лимиты запросов. Для продакшена с большой
> нагрузкой замените `utils/speech.py` на платный сервис (например, Whisper
> API от OpenAI) — интерфейс функции `transcribe_voice_file` можно оставить
> прежним.

## Возможные доработки

- Уровни сложности слов (A1–C1)
- Ежедневные напоминания и streak-система
- Экспорт/импорт словаря
- Интеграция с реальным Whisper API для более точного распознавания
