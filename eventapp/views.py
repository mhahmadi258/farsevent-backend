from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser

from .serializers import *
from .models import *


class EventCategoryView(generics.ListAPIView):
    serializer_class = EventCategorySerializer
    queryset = EventCategory.objects.all()


class EventTypeView(generics.ListAPIView):
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()


class EventCreationView(generics.CreateAPIView):
    serializer_class = EventCreationSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if isinstance(request.user,AnonymousUser):
            raise PermissionDenied('login is essential for this operation')
        serializer.save(owner= request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if isinstance(request.user,AnonymousUser):
            raise PermissionDenied('login is essential for this operation')
        serializer.save(user= request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
