from django.urls import path
from . import views

app_name = 'Chat'

urlpatterns = [
    path('', views.Chat, name='chat'),
    path('api/', views.gemini_chat_api, name='gemini_chat_api'),
    path('models/', views.list_models, name='list_models'),
    path('history/', views.chat_history, name='chat_history'),
    path('clear/', views.clear_history, name='clear_history'),
]
