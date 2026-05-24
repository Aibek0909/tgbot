from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.queries import get_top_users, get_role

router = Router()

@router.message(Command("top"))
@router.message(F.text == "🏆 Топ")
async def cmd_top(message: Message):
    users = await get_top_users(10)
    medals = ["🥇","🥈","🥉"]
    lines = ["🏆 **ТОП УЧАСТНИКОВ**\n"]
    for i, u in enumerate(users):
        m = medals[i] if i < 3 else f"#{i+1}"
        name = u["first_name"] or "Аноним"
        lines.append(f"{m} **{name}** — {get_role(u['level'])}\n    ⭐ {u['xp']} XP • Ур.{u['level']}\n")
    await message.answer("\n".join(lines))
