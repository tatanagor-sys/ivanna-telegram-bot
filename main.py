import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✨ Практики", callback_data="practices")
    )
    await message.answer("Выберите раздел:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "practices")
async def practices(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🫁 Дыхание", callback_data="breathing"),
        InlineKeyboardButton("🧘 Заземление", callback_data="grounding"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back")
    )
    await call.message.edit_text("Выберите практику:", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp)
