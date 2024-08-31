from rest_framework import serializers
from .models import Provider, Routes, Bus, Seats, Block, Book

# Provider Serializer
class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name']


class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ['id', 'route', 'provider']


class BusSerializer(serializers.ModelSerializer):
    route = RoutesSerializer(many=True)  # Nested serializer for ManyToManyField

    class Meta:
        model = Bus
        fields = "__all__"

    
class SeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = ['id', 'bus', 'total_seats', 'booked_seats', 'available_seats', 'blocked_seats']


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'block_id', 'seats_bus', 'blocked_seats']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'seats_bus', 'booked_seats']
