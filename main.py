import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # сюда будет URL Render, например https://ivanna-telegram-bot.onrender.com
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{APP_URL}{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✨ Практики", callback_data="practices")
    )
    await message.answer("Выберите раздел:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "practices")
async def practices(call: types.CallbackQuery):
    # пример “вторая ступень” кнопок
    kb = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🧘‍♀️ Антистресс (5 мин)", callback_data="p1"),
        InlineKeyboardButton("😴 Сон", callback_data="p2"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back"),
    )
    await call.message.edit_text("Практики:", reply_markup=kb)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data == "back")
async def back(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✨ Практики", callback_data="practices")
    )
    await call.message.edit_text("Выберите раздел:", reply_markup=kb)
    await call.answer()


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

app = web.Application()
# aiogram сам обработает входящие апдейты через aiohttp
executor.webhook_server(app, dp, webhook_path=WEBHOOK_PATH)

if __name__ == "__main__":
    # Render сам выдаёт PORT
    port = int(os.getenv("PORT", "10000"))
    web.run_app(app, host="0.0.0.0", port=port)
