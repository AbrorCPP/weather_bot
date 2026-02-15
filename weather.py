from requests import get
from tokens import WEATHER_API_KEY

def get_city_name(city:str):
    city = city.capitalize()
    URL = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'uzb'
    }
    response = get(URL, params=params)
    data = response.json()
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    text = "-"*20
    text += f"\nBugun {city}da Ob-havo⛅\n"
    text += f"\nHarorat {temp} °C 🌡️"
    text += f"\nMaksimal harorat {temp_max} °C"
    text += f"\nMinimal harorat {temp_min} °C"
    text += f"\nBosim {pressure} Pa"
    text += f"\nNamlik {humidity} 💧 %\n\n"
    text += "-"*20
    return text

