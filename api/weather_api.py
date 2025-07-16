# наша погода с сервера
import requests, io
from PIL import Image

URL = 'http://api.openweathermap.org/data/2.5/weather'
CITY = 'Санкт-Петербург'
KEY = '9b00cf4c643ecc72e44b4c35d8c977a4'

params = {
    'q': CITY,
    'appid': KEY,
    'units': 'metric',
    'lang': 'ru'
}

response = requests.get(URL, params=params)
print(response)
wr = response.json()
weather = wr['weather'][0]['description']
temperature = wr['main']['temp']
humidity = wr['main']['humidity']
wind = wr['wind']['speed']

data = wr['coord']
print(data)
ll = f'{data['lon']},{data['lat']}'

print(f'сегодня в городе {CITY}: {weather} Температура {temperature} Влажность {humidity}% Скорость ветра {wind} м/с')

link = f'https://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.0025,0.0025&l=map&pt={ll},pm2dgl'

# https://static-maps.yandex.ru/1.x/?ll=30.325498,59.918305&spn=0.0025,0.0025&l=map&pt=30.325498,59.918305,pm2dgl
# spn = разница между долготами
# l = режим отображения: map/sat
# для показа битовых массивов прямо из ОЗУ


image = requests.get(link).content
if image:
    im = Image.open(io.BytesIO(image)).convert('RGB')
    im.show()
    im.save('../img/map.jpg')

