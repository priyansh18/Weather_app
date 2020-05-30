import requests
from django.shortcuts import render
from .models import City
from .forms import cityForm

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0daeff595e03682a91be65b4352751d8'

    if(request.method == 'POST'):
        form = cityForm(request.POST)
        form.save()

    form = cityForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.insert(0, city_weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weatherapp/weather.html', context)
