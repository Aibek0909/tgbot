from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.queries import claim_daily, get_user, create_or_update_user
from config import XP_BONUS_DAILY, XP_BONUS_VIP

router = Router()

def hms(s):
    h, m = s // 3600, (s % 3600) // 60
    return f"{h}ч {m}м" if h else f"{m}м {s%60}с"

@router.message(Command("daily"))
@router.message(F.text == "🎁 Бонус")
async def cmd_daily(message: Message):
    user = message.from_user
    await create_or_update_user(user.id, user.username or "", user.first_name)
    u = await get_user(user.id)
    is_vip = u.get("is_vip", False) if u else False
    ok, coins, left = await claim_daily(user.id, is_vip)
    if ok:
        xp = XP_BONUS_VIP if is_vip else XP_BONUS_DAILY
        vip_tag = "\n👑 **VIP бонус x2!**" if is_vip else ""
        await message.answer(f"🎁 **Ежедневный бонус!**{vip_tag}\n\n⭐ +{xp} XP\n💰 +{coins} монет\n\nВозвращайся завтра! 🗓️")
    else:
        await message.answer(f"⏳ Бонус уже получен!\n\nСледующий через: **{hms(left)}**")
