from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, MEMBER
from database.queries import create_or_update_user
from keyboards.menus import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    await create_or_update_user(user.id, user.username or "", user.first_name)
    await message.answer(
        f"👋 **Привет, {user.first_name}!**\n\n"
        "🔹 Зарабатывай XP за сообщения\n"
        "🔹 Получай ежедневные бонусы\n"
        "🔹 Играй в мини-игры\n"
        "🔹 Попади в топ чата!\n\n"
        "Добавь меня в группу и поехали! 🚀",
        reply_markup=main_menu()
    )

@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def on_new_member(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    if user.is_bot:
        return
    await create_or_update_user(user.id, user.username or "", user.first_name)
    await event.answer(
        f"🎉 **Добро пожаловать, {user.first_name}!**\n\n"
        f"Ты в **{event.chat.title}**!\n"
        "👤 /profile — твой профиль\n"
        "🎁 /daily — ежедневный бонус\n"
        "🎮 /games — мини-игры\n\n"
        "Пиши сообщения — получай XP! 🚀"
    )
