from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def generate_cities_keyboard(cities: list) -> ReplyKeyboardMarkup:
    # cities = ["Toshkent","Fergana"]

    keyboard = ReplyKeyboardBuilder()

    for city in cities:
        keyboard.button(text=city)

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)
