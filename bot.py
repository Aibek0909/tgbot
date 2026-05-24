import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db
from middlewares.antispam import AntiSpamMiddleware
from middlewares.antiflood import AntiFloodMiddleware
from handlers import start, profile, admin, daily, top, games, levels

async def main():
    os.makedirs("logs", exist_ok=True)
    await init_db()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(AntiFloodMiddleware())
    dp.message.middleware(AntiSpamMiddleware())
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(admin.router)
    dp.include_router(daily.router)
    dp.include_router(top.router)
    dp.include_router(games.router)
    dp.include_router(levels.router)
    print("🤖 Бот запущен!")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
