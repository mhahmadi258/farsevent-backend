from rest_framework import serializers

from .models import Event , Ticket , Register , EventCategory, EventType


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = (
            'id',
            'name',
            'image',
        )


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'id',
            'name',
        )


