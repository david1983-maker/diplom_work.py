from django.shortcuts import render
import requests

from .models import City
from .forms import CityForm


# Create your views here.

def index(request):
    appid = '8bb9a681086c0e812e7c88e81a449b40'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    all_cities = []
    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()
    for city in cities:
        res = requests.get(url.format(city.name)).json()

        city_info = {

            'country': res ['sys']['country'],
            'city': city.name,
            'temp': res['main']['temp'],
            'temp_max': res['main']['temp_max'],
            'temp_min': res['main']['temp_min'],
            'icon': res['weather'][0]['icon'],
            'description': res['weather'][0]['description'],
        }
        if city_info in all_cities:
            continue


        else:
            all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'index.html', context)
