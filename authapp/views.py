from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserCreationSerializer, CitySerializer, ProfileSerializer
from .models import City


class UserCreationView(generics.CreateAPIView):
    serializer_class = UserCreationSerializer


class CityView(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        return user
