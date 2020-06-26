from django.urls import path

from .views import *

app_name = 'eventapp'

urlpatterns = [
    path('all-categories/', EventCategoryView.as_view(), name='all categoris'),
    path('all-types/', EventTypeView.as_view(), name='all types'),
]
