import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=standard&appid=6f9fe42134ece978ca12912a190da734'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    
    cities = City.objects.all()

    weather_data = list()

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    form = CityForm()

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'index.html', context)