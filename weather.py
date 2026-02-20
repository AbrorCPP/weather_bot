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
    if data["cod"] == "404":
        return None
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    text  = f"\nBugun <b>{city}</b>da Ob-havo⛅\n"
    text += f"\nHarorat<b> {temp} °C </b>🌡️"
    text += f"\nMaksimal harorat<b> {temp_max} °C</b>"
    text += f"\nMinimal harorat <b>{temp_min} °C</b>\n"
    text += f"\nBosim <b>{pressure} Pa</b> ⬇️"
    text += f"\nNamlik <b>{humidity} %</b> 💧\n\n"
    return text

