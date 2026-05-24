from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="🏆 Топ")],
        [KeyboardButton(text="🎁 Бонус"), KeyboardButton(text="🎮 Игры")],
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="ℹ️ Помощь")],
    ], resize_keyboard=True, input_field_placeholder="Выбери раздел...")

def games_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Кубик (10💰)", callback_data="game_dice"),
         InlineKeyboardButton(text="🎰 Слоты (20💰)", callback_data="game_slots")],
        [InlineKeyboardButton(text="🃏 Угадай число (15💰)", callback_data="game_guess")],
    ])
