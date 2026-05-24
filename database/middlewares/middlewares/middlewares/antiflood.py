import time
from collections import defaultdict
from aiogram import BaseMiddleware
from aiogram.types import Message
from config import FLOOD_RATE, FLOOD_PERIOD

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self):
        self._calls = defaultdict(list)

    async def __call__(self, handler, event, data):
        if not isinstance(event, Message):
            return await handler(event, data)
        uid = event.from_user.id
        now = time.time()
        self._calls[uid] = [t for t in self._calls[uid] if now - t < FLOOD_PERIOD]
        self._calls[uid].append(now)
        if len(self._calls[uid]) > FLOOD_RATE:
            return
        return await handler(event, data)
