from rest_framework import generics

from .serializers import UserCreationSerializer , CitySerializer
from .models import City



class UserCreationView(generics.CreateAPIView):
    serializer_class = UserCreationSerializer



class CityView(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()