import time
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.queries import add_warn, reset_warns
from config import ADMIN_IDS

router = Router()

def get_target(message):
    return message.reply_to_message.from_user if message.reply_to_message else None

async def is_admin(message):
    if message.from_user.id in ADMIN_IDS:
        return True
    m = await message.chat.get_member(message.from_user.id)
    return m.status in ("administrator", "creator")

@router.message(Command("warn"))
async def cmd_warn(message: Message):
    if not await is_admin(message):
        return await message.answer("🚫 Только для админов!")
    target = get_target(message)
    if not target:
        return await message.answer("❗ Ответь на сообщение пользователя")
    parts = message.text.split(maxsplit=1)
    reason = parts[1] if len(parts) > 1 else "Нарушение правил"
    warns = await add_warn(target.id, message.chat.id, message.from_user.id, reason)
    if warns >= 3:
        await message.chat.ban(user_id=target.id)
        await reset_warns(target.id)
        await message.answer(f"🔨 **{target.first_name}** забанен за {warns} варна!")
    else:
        await message.answer(f"⚠️ **{target.first_name}** получил варн [{warns}/3]\n📋 {reason}")

@router.message(Command("mute"))
async def cmd_mute(message: Message):
    if not await is_admin(message):
        return
    target = get_target(message)
    if not target:
        return await message.answer("❗ Ответь на сообщение пользователя")
    parts = message.text.split()
    mins = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
    until = int(time.time()) + mins * 60
    await message.chat.restrict(user_id=target.id, permissions={"can_send_messages": False}, until_date=until)
    await message.answer(f"🔇 **{target.first_name}** замучен на **{mins} мин.**")

@router.message(Command("unmute"))
async def cmd_unmute(message: Message):
    if not await is_admin(message):
        return
    target = get_target(message)
    if not target:
        return await message.answer("❗ Ответь на сообщение")
    await message.chat.restrict(user_id=target.id, permissions={"can_send_messages": True, "can_send_media_messages": True, "can_send_other_messages": True})
    await message.answer(f"🔊 **{target.first_name}** размучен.")

@router.message(Command("ban"))
async def cmd_ban(message: Message):
    if not await is_admin(message):
        return
    target = get_target(message)
    if not target:
        return await message.answer("❗ Ответь на сообщение")
    await message.chat.ban(user_id=target.id)
    await message.answer(f"🔨 **{target.first_name}** забанен.")

@router.message(Command("unban"))
async def cmd_unban(message: Message):
    if not await is_admin(message):
        return
    target = get_target(message)
    if not target:
        return await message.answer("❗ Ответь на сообщение")
    await message.chat.unban(user_id=target.id)
    await message.answer(f"✅ **{target.first_name}** разбанен.")
