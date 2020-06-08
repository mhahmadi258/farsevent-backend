from django.urls import path

from .views import UserCreationView

app_name = 'authapp'

urlpatterns = [
    path('create/',UserCreationView.as_view(),name='user creation'),
]