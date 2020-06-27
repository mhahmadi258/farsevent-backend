from rest_framework import serializers

from .models import Event, Ticket, Register, EventCategory, EventType


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


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'id',
            'title',
            'capacity',
            'price',
            'description',
        )


class EventSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'image',
            'description',
            'start_time',
            'end_time',
            'tags',
            'event_type',
            'event_category',
            'city',
            'address',
            'tickets',
        )

    def create(self, validated_data):
        tickets_validated_data = validated_data.pop('tickets')
        event = Event.objects.create(**validated_data)
        ticket_serializer = self.fields['tickets']
        for ticket in tickets_validated_data:
            ticket['event'] = event
        tickets = ticket_serializer.create(tickets_validated_data)
        return event

    def validate_tickets(self, value):
        if not value:
            raise serializers.ValidationError('tickets can\'t be empty')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = (
            'registration_id',
            'ticket',
        )

    extra_kwargs = {
        'registration_id': {'read_only': True},
    }


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'image',
        )
