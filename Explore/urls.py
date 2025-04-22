from django.urls import path
from . import views

app_name = 'Explore'

urlpatterns = [
    path('', views.explore_view, name='Explore'),
    path('generate_code/', views.generate_code, name='generate_code'),
    path('fix_code/', views.fix_code, name='fix_code'),
]
