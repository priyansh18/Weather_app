import requests
from django.shortcuts import render

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0daeff595e03682a91be65b4352751d8'
    city = 'Las Vegas'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    print(city_weather)

    context = {'city_weather': city_weather}

    return render(request, 'weatherapp/weather.html', context)
