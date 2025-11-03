"""Конфигурация бота"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv('BOT_TOKEN')

# База данных
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./shikimori_bot.db')

# Интервалы проверки (в минутах)
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 5))
ONLINE_CHECK_INTERVAL = int(os.getenv('ONLINE_CHECK_INTERVAL', 2))

# Shikimori
SHIKIMORI_BASE_URL = 'https://shikimori.one'
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

# Настройки по умолчанию
DEFAULT_SETTINGS = {
    'notify_history': True,
    'notify_online': False,
    'notify_offline': False,
    'notify_achievements': False,
}
