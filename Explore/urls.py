from django.urls import path
from . import views

app_name = 'Explore'

urlpatterns = [
    path('', views.Explore, name='Explore'),
    path('api/fix-code', views.fix_code, name='fix_code'),
    path('api/generate-code', views.generate_code, name='generate_code'),
]

