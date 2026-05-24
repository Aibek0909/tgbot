import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
DB_PATH = os.getenv("DB_PATH", "bot.db")

XP_PER_MESSAGE = 5
XP_BONUS_DAILY = 100
XP_BONUS_VIP = 200
VIP_DAILY_BONUS = 300
VIP_XP_MULTIPLIER = 2.0

LEVELS = {
    1:0, 2:100, 3:250, 4:500, 5:900,
    6:1400, 7:2000, 8:2800, 9:3800, 10:5000,
    15:18000, 20:30000, 30:80000, 50:200000,
}

ROLES = {
    1:"🌱 Новичок", 3:"📚 Ученик", 5:"⚡ Активист",
    8:"🔥 Ветеран", 10:"💎 Эксперт", 15:"🏆 Мастер",
    20:"👑 Легенда", 30:"🌟 Бессмертный", 50:"🚀 Бог Чата",
}

SPAM_MAX_MESSAGES = 5
SPAM_TIME_WINDOW = 5
SPAM_MUTE_DURATION = 300
FLOOD_RATE = 3
FLOOD_PERIOD = 1
