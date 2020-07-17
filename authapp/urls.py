from django.urls import path

from .views import UserCreationView, CityView, ProfileView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'authapp'

urlpatterns = [
    path('create/', UserCreationView.as_view(), name='user creation'),
    path('login/', obtain_auth_token, name='login'),
    path('all-cities/', CityView.as_view(), name='all cities'),
    path('profile/', ProfileView.as_view(), name='profile')
]
