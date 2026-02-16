from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
async def answer_weather_data(message: Message):
    city_name = message.text
    weather_data = get_city_name(city_name)

    if weather_data:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text = "Shaharni saqlash", callback_data=f"save:{city_name}")

        await message.answer(
            text=weather_data,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard.as_markup()
        )
    else:
        await message.answer(text = "Bunday shahar topilmadi")

@dp.callback_query()
async def save_city(query: CallbackQuery):
    data = query.data
    city_name = data.split(":")[-1]

    # city ... ni sqlash
    keyboard = InlineKeyboardBuilder()
    await query.answer(text = "Shahar saqlangan", show_alert=True)
    keyboard.button(text = "Shahar saqlandi ✅", callback_data="...")

    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())

@dp.callback_query(lambda call: "..." in call.data)
async def show_alert(call: CallbackQuery):
    await call.answer(text = "Shahar saqlangan", show_alert=True)

async def notfy_admins():
    for admin_id in ADMINS:
        await bot.send_message(chat_id=int(admin_id), text=f"Assalomu aleykum BOSS🕵️\nBot ishlashga tayyor🤖")


async def main():
    logging.basicConfig(level=logging.INFO)
    await notfy_admins()
    await dp.start_polling(bot)

asyncio.run(main())

