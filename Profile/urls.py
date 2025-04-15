from django.contrib import admin
from django.urls import path
from Profile import views

app_name = 'Profile'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Profile, name='Profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/', views.delete_account, name='delete_account'),
]
