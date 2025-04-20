"""
URL configuration for aichat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Chat import views as chat_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

HomePage = 'Home'

urlpatterns = [
    path('admin/', admin.site.urls),    
    # path('', views.index, name='index'),
    # path('Chat/', chat_views.Chat, name='chat'),
    path('Chat/api/', chat_views.gemini_chat_api, name='chat_api'),
    path('', include('Home.urls', namespace='Home')),
    path('About/', include('About.urls', namespace='About')),
    path('Profile/', include('Profile.urls', namespace='Profile')),
    path('Chat/', include('Chat.urls', namespace='Chat')),
    path('Explore/', include('Explore.urls', namespace='Explore')),
    path('Contact/', include('Contact.urls', namespace='Contact')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
