import requests
from pprint import pprint
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных
    """
    token = '0b6680e25e6a45208fd163951252611'  # Вставить ваш токен из api.weatherapi.com
    url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}"
    response = requests.get(url)
    data = response.json()

    pressure_mb = data['current']['pressure_mb']
    pressure_mm = round(pressure_mb * 0.75, 1)
    wind_kph = data['current']['wind_kph']
    wind_speed_ms = round(wind_kph / 3.6, 1)
    wind_gust_kph = data['current']['gust_kph']
    wind_gust_ms = round(wind_gust_kph / 3.6, 1)
    # Данная реализация приведена для api.weatherapi.com
    result = {
        'city': data['location']['name'],  # Город
        'time': data['current']['last_updated'],  # Время обновления данных
        'temp': data['current']['temp_c'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'feels_like_temp': data['current']['feelslike_c'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        'pressure': pressure_mm,  # TODO Реализовать вычисление давления из данных полученных от API
        'humidity': data['current']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'wind_speed': wind_speed_ms,  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'wind_gust': wind_gust_ms,  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['current']['wind_dir'].lower()),  # Направление ветра
    }
    return result


if __name__ == "__main__":
    pprint(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
