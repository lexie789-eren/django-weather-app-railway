from django.shortcuts import render,redirect
import requests
from django.http import JsonResponse
from .models import Weath
from django.contrib import messages
# Create your views here.

def weather(request):
    API = '293e9092e32e95690c4e4d8b4513161b'
   
    urls = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    if request.method == 'POST':
        city_name = request.POST.get('city')
        respond = requests.get(urls.format(city_name, API)).json()

        if respond['cod'] == 200:
            if not Weath.objects.filter(name = city_name).exists():
             Weath.objects.create(name = city_name)
             messages.success(request, f'{city_name} , added successfully')
            return redirect('weather')
    weather_data = []
    try:

        cities = Weath.objects.all()
        for city in cities:
            respond = requests.get(urls.format(city.name, API))
            data = respond.json()
            if data['cod'] == 200:
                
                city_weather ={
                    'city' : city.name,
                    'temperate' : data['main']['temp'],
                    'description' : data['weather'][0]['description'],
                    'icon' : data['weather'][0]['icon'],
                }
                weather_data.append(city_weather)
            else:
                Weath.objects.filter(name = city.name).delete()
    except requests.RequestException as e:
        print("error")
    
    context = {'weather' : weather_data}
    return render(request, 'index.html', context)
    