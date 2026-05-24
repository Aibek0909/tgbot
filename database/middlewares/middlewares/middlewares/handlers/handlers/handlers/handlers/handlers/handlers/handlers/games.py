import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.queries import get_user, update_coins, update_game_stats, create_or_update_user
from keyboards.menus import games_menu

router = Router()
pending_guesses = {}

@router.message(Command("games"))
@router.message(F.text == "🎮 Игры")
async def cmd_games(message: Message):
    await message.answer("🎮 **Мини-игры**\n\nВыбирай игру и испытай удачу!", reply_markup=games_menu())

@router.callback_query(F.data == "game_dice")
async def game_dice(call: CallbackQuery):
    u = await get_user(call.from_user.id)
    if not u or u["coins"] < 10:
        return await call.answer("❌ Нужно 10 монет!", show_alert=True)
    bot_r, user_r = random.randint(1,6), random.randint(1,6)
    won = user_r > bot_r
    if won:
        await update_coins(call.from_user.id, 15)
        res = f"✅ Победа! +15 💰"
    elif user_r == bot_r:
        res = "🤝 Ничья!"
    else:
        await update_coins(call.from_user.id, -10)
        res = f"❌ Проигрыш! -10 💰"
    await update_game_stats(call.from_user.id, "dice", won)
    await call.message.answer(f"🎲 Ты: **{user_r}** vs Бот: **{bot_r}**\n{res}")
    await call.answer()

@router.callback_query(F.data == "game_slots")
async def game_slots(call: CallbackQuery):
    u = await get_user(call.from_user.id)
    if not u or u["coins"] < 20:
        return await call.answer("❌ Нужно 20 монет!", show_alert=True)
    s = ["🍒","🍋","🍊","⭐","💎","7️⃣"]
    r = [random.choice(s) for _ in range(3)]
    if r[0]==r[1]==r[2]:
        prize = 200 if r[0]=="💎" else 100 if r[0]=="7️⃣" else 50
        await update_coins(call.from_user.id, prize-20)
        msg = f"✅ Три в ряд! +{prize-20} 💰"
        won = True
    else:
        await update_coins(call.from_user.id, -20)
        msg = "❌ Не повезло! -20 💰"
        won = False
    await update_game_stats(call.from_user.id, "slot", won)
    await call.message.answer(f"🎰 {''.join(r)}\n{msg}")
    await call.answer()

@router.callback_query(F.data == "game_guess")
async def game_guess(call: CallbackQuery):
    u = await get_user(call.from_user.id)
    if not u or u["coins"] < 15:
        return await call.answer("❌ Нужно 15 монет!", show_alert=True)
    pending_guesses[call.from_user.id] = random.randint(1, 10)
    await call.message.answer("🃏 Угадай число от **1 до 10**!\nСтавка: 15 💰 • Приз: 40 💰")
    await call.answer()

@router.message(F.text.regexp(r"^\d+$"))
async def handle_guess(message: Message):
    uid = message.from_user.id
    if uid not in pending_guesses:
        return
    guess = int(message.text)
    answer = pending_guesses.pop(uid)
    if guess == answer:
        await update_coins(uid, 25)
        await message.answer(f"🎉 Правильно! Число было **{answer}** • +25 💰")
    else:
        await update_coins(uid, -15)
        await message.answer(f"❌ Неверно! Число было **{answer}** • -15 💰")
