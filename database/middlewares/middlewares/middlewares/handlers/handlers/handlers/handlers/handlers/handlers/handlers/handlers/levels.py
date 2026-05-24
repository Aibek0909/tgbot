from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config import LEVELS, ROLES

router = Router()

@router.message(Command("levels"))
@router.message(F.text == "📊 Статистика")
async def cmd_levels(message: Message):
    lines = ["📊 **Система уровней**\n"]
    for lvl, xp in sorted(LEVELS.items()):
        role = ROLES.get(lvl, "")
        lines.append(f"Ур.**{lvl}** — {xp} XP {role}")
    await message.answer("\n".join(lines))
