from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.queries import get_user, create_or_update_user, add_xp, get_role, xp_to_next
from keyboards.menus import main_menu

router = Router()

def progress_bar(cur, total, length=10):
    if total == 0: return "█" * length
    filled = int(length * cur / total)
    return "█" * filled + "░" * (length - filled)

@router.message(Command("profile"))
@router.message(F.text == "👤 Профиль")
async def cmd_profile(message: Message):
    user = message.from_user
    await create_or_update_user(user.id, user.username or "", user.first_name)
    u = await get_user(user.id)
    if not u:
        await message.answer("❌ Напиши /start")
        return
    role = get_role(u["level"])
    need, total = xp_to_next(u["xp"], u["level"])
    cur = total - need
    bar = progress_bar(cur, total)
    vip = "👑 VIP\n" if u["is_vip"] else ""
    await message.answer(
        f"╔══════════════════╗\n"
        f"║ 👤 **{u['first_name']}**\n"
        f"║ {vip}"
        f"║ {role}\n"
        f"╠══════════════════╣\n"
        f"║ ⭐ XP: **{u['xp']}**\n"
        f"║ 🏅 Уровень: **{u['level']}**\n"
        f"║ 💰 Монеты: **{u['coins']}**\n"
        f"║ 💬 Сообщений: **{u['messages']}**\n"
        f"║ ⚠️ Варны: **{u['warns']}**\n"
        f"╠══════════════════╣\n"
        f"║ До ур.{u['level']+1}: {bar}\n"
        f"║ Нужно ещё {need} XP\n"
        f"╚══════════════════╝"
    )

@router.message(F.text & F.chat.type.in_({"group", "supergroup"}))
async def xp_handler(message: Message):
    if message.from_user.is_bot:
        return
    user = message.from_user
    await create_or_update_user(user.id, user.username or "", user.first_name)
    u = await get_user(user.id)
    is_vip = u.get("is_vip", False) if u else False
    new_xp, new_level, leveled_up = await add_xp(user.id, is_vip=is_vip)
    if leveled_up:
        role = get_role(new_level)
        await message.answer(
            f"🎊 **{user.first_name}** повысил уровень!\n"
            f"🏅 Уровень **{new_level}** — {role}\n"
            f"⭐ XP: **{new_xp}**"
        )
