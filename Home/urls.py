from django.urls import path
from . import views

app_name = 'Home'

urlpatterns = [
    path('', views.Home, name='Home'),
    path('animationone/', views.Animationone, name='Animationone'),
    path('animationtwo/', views.Animationtwo, name='Animationtwo'),
    path('animationthree/', views.Animationthree, name='Animationthree'),
    path('animationfour/', views.Animationfour, name='Animationfour'),
]
