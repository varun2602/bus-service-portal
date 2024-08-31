from django.contrib import admin
from .models import Provider, Routes, Bus, Seats, Block, Book

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'provider')
    search_fields = ('route',)
    list_filter = ('provider',)

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'provider', 'source', 'destination', 'date_of_journey')
    search_fields = ('name', 'source', 'destination')
    list_filter = ('provider', 'date_of_journey')
    filter_horizontal = ('route',)

@admin.register(Seats)
class SeatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'bus', 'total_seats', 'booked_seats', 'available_seats', 'blocked_seats')
    search_fields = ('bus__name',)
    list_filter = ('bus',)

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'block_id', 'seats_bus', 'blocked_seats')
    search_fields = ('block_id', 'seats_bus__bus__name',)
    list_filter = ('seats_bus',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'seats_bus', 'booked_seats')
    search_fields = ('seats_bus__bus__name',)
    list_filter = ('seats_bus',)
