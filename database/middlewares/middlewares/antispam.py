import time
from collections import defaultdict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Any, Awaitable
from config import SPAM_MAX_MESSAGES, SPAM_TIME_WINDOW, SPAM_MUTE_DURATION

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self._msgs = defaultdict(list)

    async def __call__(self, handler, event, data):
        if not isinstance(event, Message):
            return await handler(event, data)
        if event.chat.type == "private":
            return await handler(event, data)
        uid = event.from_user.id
        now = time.time()
        self._msgs[uid] = [t for t in self._msgs[uid] if now - t < SPAM_TIME_WINDOW]
        self._msgs[uid].append(now)
        if len(self._msgs[uid]) > SPAM_MAX_MESSAGES:
            try:
                await event.chat.restrict(user_id=uid, permissions={"can_send_messages": False},
                                          until_date=int(now) + SPAM_MUTE_DURATION)
                await event.answer(f"🔇 **{event.from_user.first_name}** замучен за спам на 5 минут!")
                self._msgs[uid].clear()
            except:
                pass
            return
        return await handler(event, data)
