import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import cityForm

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0daeff595e03682a91be65b4352751d8'

    err_msg = ''
    message = ''
    message_class = ''

    if(request.method == 'POST'):
        form = cityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            exisisting_city_count = City.objects.filter(name=new_city).count()
            if exisisting_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not Exist'
            else:
                err_msg = "City Already Exists in Database"

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added Sucessfully'
            message_class = 'is-success'

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

    context = {'weather_data': weather_data, 'form': form,
               'message': message, 'message_class': message_class}

    return render(request, 'weatherapp/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
