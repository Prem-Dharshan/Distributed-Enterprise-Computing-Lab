from rest_framework import serializers
from .models import Booking, Show, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'detail', 'organizer']

class ShowSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Show
        fields = ['id', 'start_time', 'end_time', 'event']

class BookingDetailSerializer(serializers.ModelSerializer):
    show = ShowSerializer()

    class Meta:
        model = Booking
        fields = '__all__'