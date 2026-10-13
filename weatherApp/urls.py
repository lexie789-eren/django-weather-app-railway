from django.urls import path
from . import views

urlpatterns = [
    path(route='app/', view= views.weather,name='weather')
]
