"""
Views for Waste Collection Management System
Full CRUD for Vehicles, Routes, Schedules + Smart-City Features:
  - Live Vehicle Tracking (GPS API)
  - Smart Waste Bin Monitoring
  - Citizen Complaint System
  - Dashboard Analytics (Chart.js data)
  - Notification System
  - Waste Type Tracking
  - Heatmap Visualization
"""

import json
import os
import random
import math
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from mongoengine.errors import NotUniqueError, ValidationError

from .models import (
    Vehicle, Route, Schedule, PickupPoint,
    WasteBin, Complaint, Notification, WasteCollection
)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════════════════════════════════════

def _unread_notif_count():
    """Returns count of unread notifications (used in context for all pages)."""
    try:
        return Notification.objects.filter(is_read=False).count()
    except Exception:
        return 0


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def dashboard(request):
    """Main dashboard showing summary statistics."""
    full_bins = WasteBin.objects.filter(fill_level__gte=80).count()
    open_complaints = Complaint.objects.filter(status='Open').count()

    context = {
        'total_vehicles':    Vehicle.objects.count(),
        'active_vehicles':   Vehicle.objects.filter(status='Active').count(),
        'total_routes':      Route.objects.count(),
        'total_schedules':   Schedule.objects.count(),
        'pending_schedules': Schedule.objects.filter(status='Pending').count(),
        'completed_schedules': Schedule.objects.filter(status='Completed').count(),
        'total_bins':        WasteBin.objects.count(),
        'full_bins':         full_bins,
        'open_complaints':   open_complaints,
        'unread_notifs':     _unread_notif_count(),
        'recent_schedules':  list(Schedule.objects.order_by('-collection_date')[:5]),
        'recent_complaints': list(Complaint.objects.order_by('-created_at')[:5]),
    }
    return render(request, 'dashboard.html', context)


# ══════════════════════════════════════════════════════════════════════════════
# VEHICLE CRUD
# ══════════════════════════════════════════════════════════════════════════════

def vehicles_list(request):
    error = None
    if request.method == 'POST':
        try:
            vehicle = Vehicle(
                vehicle_id=request.POST.get('vehicle_id', '').strip(),
                driver_name=request.POST.get('driver_name', '').strip(),
                capacity=request.POST.get('capacity', '').strip(),
                status=request.POST.get('status', 'Active'),
                waste_type=request.POST.get('waste_type', 'Mixed'),
            )
            vehicle.save()
            return redirect('vehicles_list')
        except NotUniqueError:
            error = f"Vehicle ID '{request.POST.get('vehicle_id')}' already exists."
        except ValidationError as e:
            error = str(e)

    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles.html', {
        'vehicles': vehicles,
        'error': error,
        'unread_notifs': _unread_notif_count(),
    })


def vehicle_update(request, vehicle_id):
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
            vehicle.waste_type  = request.POST.get('waste_type', 'Mixed')
            vehicle.save()
            return redirect('vehicles_list')
        except ValidationError as e:
            error = str(e)

    return render(request, 'vehicle_edit.html', {
        'vehicle': vehicle,
        'error': error,
        'unread_notifs': _unread_notif_count(),
    })


def vehicle_delete(request, vehicle_id):
    try:
        Vehicle.objects.get(vehicle_id=vehicle_id).delete()
    except Vehicle.DoesNotExist:
        pass
    return redirect('vehicles_list')


# ══════════════════════════════════════════════════════════════════════════════
# ROUTE CRUD
# ══════════════════════════════════════════════════════════════════════════════

def routes_list(request):
    error = None
    if request.method == 'POST':
        try:
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
    return render(request, 'routes.html', {
        'routes': routes,
        'error': error,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
        'unread_notifs': _unread_notif_count(),
    })


def route_update(request, route_id):
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
        'unread_notifs': _unread_notif_count(),
    })


def route_delete(request, route_id):
    try:
        Route.objects.get(route_id=route_id).delete()
    except Route.DoesNotExist:
        pass
    return redirect('routes_list')


# ══════════════════════════════════════════════════════════════════════════════
# SCHEDULE CRUD
# ══════════════════════════════════════════════════════════════════════════════

def schedules_list(request):
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
        'unread_notifs': _unread_notif_count(),
    })


def schedule_update(request, schedule_id):
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
        'unread_notifs': _unread_notif_count(),
    })


def schedule_delete(request, schedule_id):
    try:
        Schedule.objects.get(schedule_id=schedule_id).delete()
    except Schedule.DoesNotExist:
        pass
    return redirect('schedules_list')


# ══════════════════════════════════════════════════════════════════════════════
# MAP VIEW (Enhanced with live tracking, bins, heatmap)
# ══════════════════════════════════════════════════════════════════════════════

def map_view(request):
    routes = Route.objects.all()
    routes_json = json.dumps([r.to_dict() for r in routes])
    vehicles_json = json.dumps([v.to_dict() for v in Vehicle.objects.filter(status='Active')])
    bins_json = json.dumps([b.to_dict() for b in WasteBin.objects.all()])
    return render(request, 'map.html', {
        'routes_json':   routes_json,
        'vehicles_json': vehicles_json,
        'bins_json':     bins_json,
        'maps_key':      settings.GOOGLE_MAPS_API_KEY,
        'unread_notifs': _unread_notif_count(),
    })


# ══════════════════════════════════════════════════════════════════════════════
# WASTE BIN MONITORING
# ══════════════════════════════════════════════════════════════════════════════

def bins_list(request):
    """Waste bin monitoring page."""
    error = None
    if request.method == 'POST':
        try:
            bin_obj = WasteBin(
                bin_id=request.POST.get('bin_id', '').strip(),
                area=request.POST.get('area', '').strip(),
                lat=float(request.POST.get('lat', 13.0827)),
                lng=float(request.POST.get('lng', 80.2707)),
                fill_level=int(request.POST.get('fill_level', 0)),
                waste_type=request.POST.get('waste_type', 'General'),
            )
            bin_obj.save()
            return redirect('bins_list')
        except NotUniqueError:
            error = f"Bin ID '{request.POST.get('bin_id')}' already exists."
        except (ValidationError, ValueError) as e:
            error = str(e)

    bins = WasteBin.objects.all()
    full_count   = sum(1 for b in bins if b.fill_level >= 80)
    half_count   = sum(1 for b in bins if 50 <= b.fill_level < 80)
    low_count    = sum(1 for b in bins if b.fill_level < 50)
    return render(request, 'bins.html', {
        'bins': bins,
        'full_count': full_count,
        'half_count': half_count,
        'low_count':  low_count,
        'error': error,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
        'unread_notifs': _unread_notif_count(),
    })


def bin_delete(request, bin_id):
    try:
        WasteBin.objects.get(bin_id=bin_id).delete()
    except WasteBin.DoesNotExist:
        pass
    return redirect('bins_list')


# ══════════════════════════════════════════════════════════════════════════════
# COMPLAINT SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

def complaints_list(request):
    """Complaint list + new complaint submission."""
    error = None
    if request.method == 'POST':
        try:
            # Handle image upload
            image_path = ''
            if 'image' in request.FILES:
                img = request.FILES['image']
                media_dir = os.path.join(settings.MEDIA_ROOT, 'complaints')
                os.makedirs(media_dir, exist_ok=True)
                filename = f"complaint_{datetime.now().strftime('%Y%m%d%H%M%S')}_{img.name}"
                filepath = os.path.join(media_dir, filename)
                with open(filepath, 'wb+') as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                image_path = f"complaints/{filename}"

            # Auto-generate complaint ID
            count = Complaint.objects.count()
            complaint_id = f"C{str(count + 1).zfill(3)}"

            complaint = Complaint(
                complaint_id=complaint_id,
                category=request.POST.get('category', 'Other'),
                description=request.POST.get('description', '').strip(),
                image_path=image_path,
                lat=float(request.POST.get('lat', 13.0827)),
                lng=float(request.POST.get('lng', 80.2707)),
                address=request.POST.get('address', '').strip(),
                reporter_name=request.POST.get('reporter_name', 'Anonymous').strip(),
            )
            complaint.save()

            # Create notification for new complaint
            Notification(
                title='New Complaint Received',
                message=f"Complaint #{complaint_id}: {complaint.category} reported by {complaint.reporter_name}.",
                notif_type='warning',
            ).save()

            return redirect('complaints_list')
        except (ValidationError, ValueError) as e:
            error = str(e)

    complaints = Complaint.objects.all()
    categories = Complaint.CATEGORIES
    return render(request, 'complaints.html', {
        'complaints': complaints,
        'categories': categories,
        'error': error,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
        'unread_notifs': _unread_notif_count(),
    })


def complaint_detail(request, complaint_id):
    """Admin detail/resolve view for a single complaint."""
    try:
        complaint = Complaint.objects.get(complaint_id=complaint_id)
    except Complaint.DoesNotExist:
        return redirect('complaints_list')

    error = None
    if request.method == 'POST':
        try:
            complaint.status     = request.POST.get('status', complaint.status)
            complaint.admin_note = request.POST.get('admin_note', '').strip()
            if complaint.status in ('Resolved', 'Closed') and not complaint.resolved_at:
                complaint.resolved_at = datetime.utcnow()
            complaint.save()

            if complaint.status == 'Resolved':
                Notification(
                    title='Complaint Resolved',
                    message=f"Complaint #{complaint_id} has been resolved.",
                    notif_type='success',
                ).save()

            return redirect('complaints_list')
        except ValidationError as e:
            error = str(e)

    return render(request, 'complaint_detail.html', {
        'complaint': complaint,
        'statuses': Complaint.STATUSES,
        'error': error,
        'maps_key': settings.GOOGLE_MAPS_API_KEY,
        'unread_notifs': _unread_notif_count(),
    })


# ══════════════════════════════════════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════════════════

def notifications_view(request):
    """Notification listing page."""
    if request.method == 'POST' and request.POST.get('action') == 'mark_all_read':
        Notification.objects(is_read=False).update(set__is_read=True)
        return redirect('notifications_view')

    notifications = Notification.objects.order_by('-created_at')[:50]
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_notifs': _unread_notif_count(),
    })


# ══════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

def analytics_view(request):
    """Analytics dashboard page."""
    return render(request, 'analytics.html', {
        'unread_notifs': _unread_notif_count(),
    })


# ══════════════════════════════════════════════════════════════════════════════
# JSON API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

def api_routes(request):
    """Return all routes with pickup points as JSON."""
    routes = [r.to_dict() for r in Route.objects.all()]
    return JsonResponse({'routes': routes})


def api_bins(request):
    """Return all waste bins as JSON."""
    bins = [b.to_dict() for b in WasteBin.objects.all()]
    return JsonResponse({'bins': bins})


def api_vehicle_locations(request):
    """Return current GPS positions for all active vehicles."""
    vehicles = [v.to_dict() for v in Vehicle.objects.filter(status='Active')]
    return JsonResponse({'vehicles': vehicles})


@csrf_exempt
@require_POST
def api_update_vehicle_location(request, vehicle_id):
    """Update a vehicle's GPS coordinates (called by tracking simulation)."""
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
        data = json.loads(request.body)
        vehicle.current_lat = float(data.get('lat', vehicle.current_lat))
        vehicle.current_lng = float(data.get('lng', vehicle.current_lng))
        vehicle.last_location_update = datetime.utcnow()
        vehicle.save()
        return JsonResponse({'status': 'ok', 'lat': vehicle.current_lat, 'lng': vehicle.current_lng})
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    except (ValueError, json.JSONDecodeError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_POST
def api_simulate_vehicle_movement(request):
    """
    Simulate vehicle movement for demo purposes.
    Nudges all active vehicles slightly toward their assigned route points.
    """
    vehicles = Vehicle.objects.filter(status='Active')
    updated = []
    for v in vehicles:
        # Small random drift around Chennai
        delta_lat = (random.random() - 0.5) * 0.004
        delta_lng = (random.random() - 0.5) * 0.004
        v.current_lat = round(v.current_lat + delta_lat, 6)
        v.current_lng = round(v.current_lng + delta_lng, 6)
        v.last_location_update = datetime.utcnow()
        v.save()
        updated.append({'vehicle_id': v.vehicle_id, 'lat': v.current_lat, 'lng': v.current_lng})
    return JsonResponse({'updated': updated})


def api_notifications(request):
    """Return recent unread notifications as JSON (for polling)."""
    notifs = [n.to_dict() for n in Notification.objects.filter(is_read=False).order_by('-created_at')[:10]]
    return JsonResponse({'notifications': notifs, 'count': len(notifs)})


@csrf_exempt
@require_POST
def api_mark_notifications_read(request):
    """Mark all notifications as read."""
    Notification.objects(is_read=False).update(set__is_read=True)
    return JsonResponse({'status': 'ok'})


def api_analytics(request):
    """
    Return analytics data for Chart.js charts:
    - waste_by_area: tonnes collected per area
    - daily_pickups: schedule completions per day (last 7 days)
    - vehicle_status: count by status
    - waste_type_distribution: by waste type
    """
    # Waste collected per area
    collections = WasteCollection.objects.all()
    area_data = {}
    for c in collections:
        area_data[c.area] = area_data.get(c.area, 0) + c.tonnes_collected
    area_labels = list(area_data.keys())
    area_values = [area_data[a] for a in area_labels]

    # Daily pickup completion (last 7 days)
    today = datetime.now().date()
    daily_labels = []
    daily_values = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        count = Schedule.objects.filter(collection_date=day_str, status='Completed').count()
        daily_labels.append(day.strftime('%b %d'))
        daily_values.append(count)

    # Vehicle status breakdown
    statuses = ['Active', 'Inactive', 'Under Maintenance']
    vehicle_status_data = [Vehicle.objects.filter(status=s).count() for s in statuses]

    # Waste type distribution from collections
    waste_types = ['General', 'Organic', 'Plastic', 'Metal', 'Mixed']
    waste_type_data = []
    for wt in waste_types:
        total = sum(c.tonnes_collected for c in WasteCollection.objects.filter(waste_type=wt))
        waste_type_data.append(round(total, 2))

    # Bin fill levels
    bins = WasteBin.objects.all()
    bin_stats = {
        'full': sum(1 for b in bins if b.fill_level >= 80),
        'half': sum(1 for b in bins if 50 <= b.fill_level < 80),
        'low':  sum(1 for b in bins if b.fill_level < 50),
    }

    return JsonResponse({
        'waste_by_area': {
            'labels': area_labels,
            'data':   area_values,
        },
        'daily_pickups': {
            'labels': daily_labels,
            'data':   daily_values,
        },
        'vehicle_status': {
            'labels': statuses,
            'data':   vehicle_status_data,
        },
        'waste_type_distribution': {
            'labels': waste_types,
            'data':   waste_type_data,
        },
        'bin_fill_stats': bin_stats,
    })
