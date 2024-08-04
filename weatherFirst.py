import eel
from bs4 import BeautifulSoup
import requests

eel.init('weather_web')

@eel.expose
def weather_check(city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    res = requests.get(
        f'https://www.google.com/search?q={city} погода&oq={city} погода&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers
    )

    soup = BeautifulSoup(res.text, 'html.parser')

    # Получаем данные
    temperature = soup.select_one('#wob_tm').get_text().strip()
    precipitation = soup.select_one('#wob_dc').get_text().strip()

    precipitation_rus = {'Sunny': 'Солнечно', 'Clear': 'Ясно', 'Partly Cloudy': 'Малооблачно', 'Cloudy': 'Облачно',
                         'Overcast': 'Пасмурно', 'Rain': 'Дождь', 'Snow': 'Снег', 'Downpour': 'Ливень',
                         'Thunderstorm': 'Гроза', 'Fog': 'Туман', 'Hail': 'Град', 'Blizzard': 'Метель',
                         'Drizzle': 'Морось', 'Variable Clouds': 'Переменная облачность',
                         'Partly cloudy': 'Переменная облачность', 'Light rain showers': 'Небольшие ливневые дожди', 'Mostly cloudy': 'В основном облачно', 'Mostly sunny': 'В основном солнечная'}

    weather_smile = {'Sunny': '☀️', 'Clear': '☀️', 'Partly Cloudy': '🌤', 'Cloudy': '🌥', 'Overcast': '⛅', 'Rain': '🌧', 'Snow': '🌨',
                     'Downpour': '⛈', 'Thunderstorm': '🌩', 'Fog': '🌫', 'Hail': '☄', 'Blizzard': '🌪️', 'Drizzle': '🌦', 'Variable Clouds': '🌤',
                     'Partly cloudy': '🌤', 'Light rain showers': '☔', 'Mostly cloudy': '⛅', 'Mostly sunny': '⛅'}

    # Возвращаем объект с данными
    return {
        'temperature': f"{temperature}°C",
        'precipitation': precipitation_rus.get(precipitation, precipitation),
        'weather_smile': weather_smile.get(precipitation, precipitation)
    }

eel.start("weather_app.html", size=(900,600))
