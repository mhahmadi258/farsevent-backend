from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django.core.exceptions import PermissionDenied ,ValidationError
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .serializers import *
from .models import *
from .decoder import decode_ticket


class EventCategoryView(generics.ListAPIView):
    serializer_class = EventCategorySerializer
    queryset = EventCategory.objects.all()


class EventTypeView(generics.ListAPIView):
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()


class EventCreationView(generics.CreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'tickets' in data.keys():
            data['tickets'] = decode_ticket(data['tickets'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if isinstance(request.user, AnonymousUser):
            raise PermissionDenied('login is essential for this operation')
        serializer.save(owner=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if isinstance(request.user, AnonymousUser):
            raise PermissionDenied('login is essential for this operation')
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventListView(generics.ListAPIView):
    serializer_class = EventListSerializer
    queryset = Event.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['event_category', 'event_type', 'city']
    ordering_fields = ['title']
    pagination_class = LimitOffsetPagination


class EventView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = 'id'


class ProfileEventShowView(generics.ListAPIView):
    serializer_class = ProfileEventShowSerailizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Register.objects.filter(user=user)
