"""
Register models with Django Admin for easy data management via /admin interface.
"""

from django.contrib import admin
from .models import Vehicle, Route, Schedule


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display  = ['vehicle_id', 'driver_name', 'capacity', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['vehicle_id', 'driver_name']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display  = ['route_id', 'area', 'pickup_count', 'created_at']
    search_fields = ['route_id', 'area']
    
    def pickup_count(self, obj):
        return obj.pickup_count
    pickup_count.short_description = 'Pickup Points'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display  = ['schedule_id', 'vehicle', 'route', 'collection_date', 'status']
    list_filter   = ['status', 'collection_date']
    search_fields = ['schedule_id']
