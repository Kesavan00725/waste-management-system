"""
Views for Waste Collection Management System
Implements full CRUD for Vehicles, Routes, and Schedules.
All data is stored in MongoDB via MongoEngine.
"""

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from mongoengine.errors import NotUniqueError, ValidationError

from .models import Vehicle, Route, Schedule, PickupPoint


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def dashboard(request):
    """Main dashboard showing summary statistics."""
    context = {
        'total_vehicles':  Vehicle.objects.count(),
        'active_vehicles': Vehicle.objects.filter(status='Active').count(),
        'total_routes':    Route.objects.count(),
        'total_schedules': Schedule.objects.count(),
        'pending_schedules':   Schedule.objects.filter(status='Pending').count(),
        'completed_schedules': Schedule.objects.filter(status='Completed').count(),
        'recent_schedules': list(Schedule.objects.order_by('-collection_date')[:5]),
    }
    return render(request, 'dashboard.html', context)


# ══════════════════════════════════════════════════════════════════════════════
# VEHICLE CRUD
# ══════════════════════════════════════════════════════════════════════════════

def vehicles_list(request):
    """List all vehicles and handle Create via POST."""
    error = None
    if request.method == 'POST':
        try:
            vehicle = Vehicle(
                vehicle_id=request.POST.get('vehicle_id', '').strip(),
                driver_name=request.POST.get('driver_name', '').strip(),
                capacity=request.POST.get('capacity', '').strip(),
                status=request.POST.get('status', 'Active'),
            )
            vehicle.save()
            return redirect('vehicles_list')
        except NotUniqueError:
            error = f"Vehicle ID '{request.POST.get('vehicle_id')}' already exists."
        except ValidationError as e:
            error = str(e)

    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles.html', {'vehicles': vehicles, 'error': error})


def vehicle_update(request, vehicle_id):
    """Update an existing vehicle."""
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
    except Vehicle.DoesNotExist:
        return redirect('vehicles_list')

    error = None
    if request.method == 'POST':
        try:
            vehicle.driver_name = request.POST.get('driver_name', '').strip()
            vehicle.capacity    = request.POST.get('capacity', '').strip()
            vehicle.status      = request.POST.get('status', 'Active')
            vehicle.save()
            return redirect('vehicles_list')
        except ValidationError as e:
            error = str(e)

    return render(request, 'vehicle_edit.html', {'vehicle': vehicle, 'error': error})


def vehicle_delete(request, vehicle_id):
    """Delete a vehicle by vehicle_id."""
    try:
        Vehicle.objects.get(vehicle_id=vehicle_id).delete()
    except Vehicle.DoesNotExist:
        pass
    return redirect('vehicles_list')


# ══════════════════════════════════════════════════════════════════════════════
# ROUTE CRUD
# ══════════════════════════════════════════════════════════════════════════════

def routes_list(request):
    """List all routes and handle Create via POST."""
    error = None
    if request.method == 'POST':
        try:
            # Parse pickup points from JSON string submitted by JS
            raw_points = request.POST.get('pickup_points', '[]')
            points_data = json.loads(raw_points)
            pickup_points = [
                PickupPoint(lat=float(p['lat']), lng=float(p['lng']))
                for p in points_data
                if 'lat' in p and 'lng' in p
            ]
            route = Route(
                route_id=request.POST.get('route_id', '').strip(),
                area=request.POST.get('area', '').strip(),
                pickup_points=pickup_points,
            )
            route.save()
            return redirect('routes_list')
        except NotUniqueError:
            error = f"Route ID '{request.POST.get('route_id')}' already exists."
        except (ValidationError, json.JSONDecodeError, ValueError) as e:
            error = f"Error saving route: {e}"

    routes = Route.objects.all()
    return render(request, 'routes.html', {'routes': routes, 'error': error,
                                            'maps_key': settings.GOOGLE_MAPS_API_KEY})


def route_update(request, route_id):
    """Update an existing route."""
    try:
        route = Route.objects.get(route_id=route_id)
    except Route.DoesNotExist:
        return redirect('routes_list')

    error = None
    if request.method == 'POST':
        try:
            raw_points = request.POST.get('pickup_points', '[]')
            points_data = json.loads(raw_points)
            route.area = request.POST.get('area', '').strip()
            route.pickup_points = [
                PickupPoint(lat=float(p['lat']), lng=float(p['lng']))
                for p in points_data
            ]
            route.save()
            return redirect('routes_list')
        except (ValidationError, json.JSONDecodeError, ValueError) as e:
            error = str(e)

    return render(request, 'route_edit.html', {
        'route': route,
        'error': error,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
        'pickup_points_json': json.dumps([p.to_dict() for p in route.pickup_points]),
    })


def route_delete(request, route_id):
    """Delete a route by route_id."""
    try:
        Route.objects.get(route_id=route_id).delete()
    except Route.DoesNotExist:
        pass
    return redirect('routes_list')


# ══════════════════════════════════════════════════════════════════════════════
# SCHEDULE CRUD
# ══════════════════════════════════════════════════════════════════════════════

def schedules_list(request):
    """List all schedules and handle Create via POST."""
    error = None
    if request.method == 'POST':
        try:
            schedule = Schedule(
                schedule_id=request.POST.get('schedule_id', '').strip(),
                vehicle_id=request.POST.get('vehicle_id', '').strip(),
                route_id=request.POST.get('route_id', '').strip(),
                collection_date=request.POST.get('collection_date', '').strip(),
                status=request.POST.get('status', 'Pending'),
            )
            schedule.save()
            return redirect('schedules_list')
        except NotUniqueError:
            error = f"Schedule ID '{request.POST.get('schedule_id')}' already exists."
        except ValidationError as e:
            error = str(e)

    schedules = Schedule.objects.all()
    vehicles  = Vehicle.objects.only('vehicle_id', 'driver_name')
    routes    = Route.objects.only('route_id', 'area')
    return render(request, 'schedules.html', {
        'schedules': schedules,
        'vehicles': vehicles,
        'routes': routes,
        'error': error,
    })


def schedule_update(request, schedule_id):
    """Update an existing schedule."""
    try:
        schedule = Schedule.objects.get(schedule_id=schedule_id)
    except Schedule.DoesNotExist:
        return redirect('schedules_list')

    vehicles = Vehicle.objects.only('vehicle_id', 'driver_name')
    routes   = Route.objects.only('route_id', 'area')
    error    = None

    if request.method == 'POST':
        try:
            schedule.vehicle_id      = request.POST.get('vehicle_id', '').strip()
            schedule.route_id        = request.POST.get('route_id', '').strip()
            schedule.collection_date = request.POST.get('collection_date', '').strip()
            schedule.status          = request.POST.get('status', 'Pending')
            schedule.save()
            return redirect('schedules_list')
        except ValidationError as e:
            error = str(e)

    return render(request, 'schedule_edit.html', {
        'schedule': schedule,
        'vehicles': vehicles,
        'routes': routes,
        'error': error,
    })


def schedule_delete(request, schedule_id):
    """Delete a schedule by schedule_id."""
    try:
        Schedule.objects.get(schedule_id=schedule_id).delete()
    except Schedule.DoesNotExist:
        pass
    return redirect('schedules_list')


# ══════════════════════════════════════════════════════════════════════════════
# MAP VIEW
# ══════════════════════════════════════════════════════════════════════════════

def map_view(request):
    """
    Renders the Google Maps page.
    All routes and their pickup_points are passed as JSON to the template
    so the JavaScript can render markers and polylines.
    """
    routes = Route.objects.all()
    routes_json = json.dumps([r.to_dict() for r in routes])
    return render(request, 'map.html', {
        'routes_json': routes_json,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
    })


# ══════════════════════════════════════════════════════════════════════════════
# JSON API ENDPOINTS (used by AJAX / map page)
# ══════════════════════════════════════════════════════════════════════════════

def api_routes(request):
    """Return all routes with pickup points as JSON (for map rendering)."""
    routes = [r.to_dict() for r in Route.objects.all()]
    return JsonResponse({'routes': routes})
