from rest_framework import generics

from .serializers import UserCreationSerializer



class UserCreationView(generics.CreateAPIView):
    serializer_class = UserCreationSerializer

