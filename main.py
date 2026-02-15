from aiogram.types import Message
from aiogram import Dispatcher,Bot
from tokens import BOT_TOKEN,ADMINS
from DB_conn import register_user
from weather import get_city_name
import logging
import asyncio

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

@dp.message(lambda message: message.text == "/start")
async def register(message: Message):
    try:
        register_user(message.from_user.id, message.from_user.full_name)
        t1 = f"Assalomu aleykum {message.from_user.full_name}\n"
        t1 += "Botimizga hush kelibsiz😊\n"
        t1 += "Botimiz shahar, viloyat va davlat 🏙️\n"
        t1 += "Ob-havosi haqida ma'lumot beradi⛅\n"
        t1 += "Nomini kiritsangiz bo'ldi.🤖"
        await message.answer(text=t1)
    except Exception as e:
        await message.answer(text=f"Siz bazada mavjudisiz✨\nXatolik: {e}")

@dp.message()
async def taker(message: Message):
    try:
        text = get_city_name(message.text)
        await message.answer(text)
    except:
        await message.answer("Yuborilgan text shahar nomi emas.⛔")

async def notfy_admins():
    for admin_id in ADMINS:
        await bot.send_message(chat_id=int(admin_id), text=f"Assalomu aleykum BOSS🕵️\nBot ishlashga tayyor🤖")


async def main():
    logging.basicConfig(level=logging.INFO)
    await notfy_admins()
    await dp.start_polling(bot)

asyncio.run(main())

