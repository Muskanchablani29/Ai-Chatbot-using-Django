from django.urls import path
from . import views

app_name = 'Home'

urlpatterns = [
    path('', views.Home, name='Home'),
    path('Animationone/', views.Animationone, name='Animationone'),
    path('Animationtwo/', views.Animationtwo, name='Animationtwo'),
    path('Animationthree/', views.Animationthree, name='Animationthree'),
    path('Animationfour/', views.Animationfour, name='Animationfour'),
]
