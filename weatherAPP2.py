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
    time = soup.select('#wob_dts')[0].getText().strip()
    temperature = soup.select_one('#wob_tm').get_text().strip()
    precipitation = soup.select_one('#wob_dc').get_text().strip()
    pro_addi = soup.select('#wob_pp')[0].getText().strip()
    humidity = soup.select('#wob_hm')[0].getText().strip()
    wind= soup.select('#wob_ws')[0].getText().strip()


    day_rus = {'дүйсенбі': 'Понедельник', 'сейсенбі': 'Вторник', 'сәрсенбі': 'Среда', 'бейсенбі': 'Четверг',
               'жұма': 'Пятница', 'сенбі': 'Суббота', 'жексенбі': 'Воскресенье'}
    day = day_rus.get(time[0:-6], time[0:-6])


    if time[-5:-4] != '0':
        time1 = time[-5:-3]
    else:
        time1 = time[-4:-3]

    if int(time[-5:-3]) >= 6 and int(time[-5:-3]) <= 19:
        time_img = 'https://cdn-icons-png.flaticon.com/512/4814/4814268.png'
    else:
        time_img = 'https://cdn-icons-png.flaticon.com/512/3662/3662525.png'


    precipitation_rus = {'Sunny': 'Солнечно', 'Clear': 'Ясно', 'Partly Cloudy': 'Малооблачно', 'Cloudy': 'Облачно',
                         'Overcast': 'Пасмурно', 'Rain': 'Дождь', 'Snow': 'Снег', 'Downpour': 'Ливень',
                         'Thunderstorm': 'Гроза', 'Fog': 'Туман', 'Hail': 'Град', 'Blizzard': 'Метель',
                         'Drizzle': 'Морось', 'Variable Clouds': 'Переменная облачность',
                         'Partly cloudy': 'Переменная облачность', 'Light rain showers': 'Небольшие ливневые дожди',
                         'Mostly cloudy': 'В основном облачно', 'Mostly sunny': 'В основном солнечная',
                         'Clear with periodic clouds': 'Ясно, временами облачно','Heavy thunderstorm': 'Сильная гроза', 'Partly sunny': 'Местами солнечно'}

    #погода flaticon Freepik солне и облако
    weather_img = {'Sunny': 'https://cdn-icons-png.flaticon.com/512/4810/4810371.png',
                     'Clear': 'https://cdn-icons-png.flaticon.com/512/4814/4814275.png',
                     'Partly Cloudy': 'https://cdn-icons-png.flaticon.com/512/5903/5903939.png',
                     'Cloudy': 'https://cdn-icons-png.flaticon.com/512/5903/5903939.png',
                     'Overcast': 'https://cdn-icons-png.flaticon.com/512/1542/1542627.png',
                     'Rain': 'https://cdn-icons-png.flaticon.com/512/8841/8841410.png',
                     'Snow': 'https://cdn-icons-png.flaticon.com/512/3730/3730830.png',
                     'Downpour': 'https://cdn-icons-png.flaticon.com/512/8841/8841374.png',
                     'Thunderstorm': 'https://cdn-icons-png.flaticon.com/512/4151/4151040.png',
                     'Fog': 'https://cdn-icons-png.flaticon.com/512/3750/3750480.png',
                     'Hail': 'https://cdn-icons-png.flaticon.com/512/5903/5903457.png',
                     'Blizzard': 'https://cdn-icons-png.flaticon.com/512/11016/11016050.png',
                     'Drizzle': 'https://cdn-icons-png.flaticon.com/512/3767/3767036.png',
                     'Variable Clouds': 'https://cdn-icons-png.flaticon.com/512/1574/1574213.png',
                     'Partly cloudy': 'https://cdn-icons-png.flaticon.com/512/1574/1574213.png',
                     'Light rain showers': 'https://cdn-icons-png.flaticon.com/512/8841/8841410.png',
                     'Mostly cloudy': 'https://cdn-icons-png.flaticon.com/512/5903/5903939.png',
                     'Mostly sunny': 'https://cdn-icons-png.flaticon.com/512/5243/5243810.png',
                     'Clear with periodic clouds': 'https://cdn-icons-png.flaticon.com/512/9537/9537005.png',
                     'Heavy thunderstorm': 'https://cdn-icons-png.flaticon.com/512/4151/4151040.png',
                     'Partly sunny': 'https://cdn-icons-png.flaticon.com/512/5243/5243810.png'
                   }

    # Возвращаем объект с данными
    return {
        'temperature': f"{temperature}°C",
        'precipitation': precipitation_rus.get(precipitation, precipitation),
        'weather_img': weather_img.get(precipitation, ''),
        'day': day,
        'time': f'{time1} ч.',
        'time_img': time_img,
        'pro_addi': pro_addi,
        'humidity': humidity,
        'wind': wind[0:2],
        'wind_s': 'км/ч'
    }

eel.start("weather_app.html", size=(900,600))
