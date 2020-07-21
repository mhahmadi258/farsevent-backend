from django.urls import path

from .views import *

app_name = 'eventapp'

urlpatterns = [
    path('all-categories/', EventCategoryView.as_view(), name='all categoris'),
    path('all-types/', EventTypeView.as_view(), name='all types'),
    path('create-event/', EventCreationView.as_view(), name='event creation'),
    path('register/', RegisterView.as_view(), name='register'),
    path('event-list/', EventListView.as_view(), name='event list'),
    path('event/<int:id>/', EventView.as_view(), name='event'),
    path('profile/event-list/', ProfileEventShowView.as_view(), name='profile event'),
]
