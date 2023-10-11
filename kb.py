from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
menu = [
    [InlineKeyboardButton(text="📝 Выбрать ссылку для мониторинга", callback_data="paste_url")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
ok = [
    [InlineKeyboardButton(text="📝 Сохранить", callback_data="save")]
]
ok = InlineKeyboardMarkup(inline_keyboard=ok)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])