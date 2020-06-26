from rest_framework import generics

from .serializer import EventCategorySerializer , EventTypeSerializer
from .models import EventCategory , EventType

class EventCategoryView(generics.ListAPIView):
    serializer_class = EventCategorySerializer
    queryset = EventCategory.objects.all()


class EventTypeView(generics.ListAPIView):
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()

