from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Dispatcher,Bot
from tokens import BOT_TOKEN,ADMINS
from DB_conn import *
from weather import get_city_name
from keyboard import generate_cities_keyboard
import logging
import asyncio

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

@dp.message(lambda message: message.text == "/start")
async def register(message: Message):
    if check_if_user_id_available(message.from_user.id):
        register_user(str(message.from_user.id), message.from_user.full_name)
        t1 = f"Assalomu aleykum {message.from_user.full_name}\n"
        t1 += "Botimizga hush kelibsiz😊\n"
        t1 += "Botimiz shahar, viloyat va davlat 🏙️\n"
        t1 += "Ob-havosi haqida ma'lumot beradi⛅\n"
        t1 += "Nomini kiritsangiz bo'ldi.🤖"
        await message.answer(text=t1)
    else:
        await message.answer(text=f"Bazada mavjudisiz✨\n")


@dp.message(lambda message: message.text == "/saved")
async def saved_city(message: Message):
    telegram_id = str(message.from_user.id)
    cities = get_user_cities(int(telegram_id))

    await message.answer(text = "Salom")

    if not cities:
        await message.answer("Sizda hali saqlangan shahar yo‘q ❌")
        return

    await message.answer(
        text="Saqlangan shaharlar:",
        reply_markup=generate_cities_keyboard(cities)
    )

@dp.message(lambda message: message.text == "/clear_saved")
async def clear_saved_city(message: Message):
    telegram_id = message.from_user.id
    delete_from_user_cities(telegram_id)
    await message.answer(text="Barcha shaharlar o'chirildi🏙️",reply_markup = ReplyKeyboardRemove())


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
        await message.answer(text = "Bunday shahar topilmadi🏙️")

@dp.callback_query()
async def save_city(query: CallbackQuery):
    data = query.data
    city_name = data.split(":")[-1]

    register_city(
        telegram_id=query.from_user.id,
        city_name=city_name,
    )
    # city ... ni sqlash
    keyboard = InlineKeyboardBuilder()
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

