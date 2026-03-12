"""
URL patterns for Waste Management app — including all Smart-City features
"""
from django.urls import path
from . import views

urlpatterns = [
    # ── Dashboard ────────────────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),

    # ── Vehicles ─────────────────────────────────────────────────────
    path('vehicles/',                         views.vehicles_list,   name='vehicles_list'),
    path('vehicles/edit/<str:vehicle_id>/',   views.vehicle_update,  name='vehicle_update'),
    path('vehicles/delete/<str:vehicle_id>/', views.vehicle_delete,  name='vehicle_delete'),

    # ── Routes ───────────────────────────────────────────────────────
    path('routes/',                       views.routes_list,   name='routes_list'),
    path('routes/edit/<str:route_id>/',   views.route_update,  name='route_update'),
    path('routes/delete/<str:route_id>/', views.route_delete,  name='route_delete'),

    # ── Schedules ────────────────────────────────────────────────────
    path('schedules/',                          views.schedules_list,   name='schedules_list'),
    path('schedules/edit/<str:schedule_id>/',   views.schedule_update,  name='schedule_update'),
    path('schedules/delete/<str:schedule_id>/', views.schedule_delete,  name='schedule_delete'),

    # ── Map (Enhanced) ───────────────────────────────────────────────
    path('map/', views.map_view, name='map_view'),

    # ── Waste Bins ───────────────────────────────────────────────────
    path('bins/',                       views.bins_list,   name='bins_list'),
    path('bins/delete/<str:bin_id>/',   views.bin_delete,  name='bin_delete'),

    # ── Complaints ───────────────────────────────────────────────────
    path('complaints/',                              views.complaints_list,  name='complaints_list'),
    path('complaints/<str:complaint_id>/',           views.complaint_detail, name='complaint_detail'),

    # ── Notifications ────────────────────────────────────────────────
    path('notifications/', views.notifications_view, name='notifications_view'),

    # ── Analytics ────────────────────────────────────────────────────
    path('analytics/', views.analytics_view, name='analytics_view'),

    # ── JSON API Endpoints ───────────────────────────────────────────
    path('api/routes/',                                     views.api_routes,                    name='api_routes'),
    path('api/bins/',                                       views.api_bins,                      name='api_bins'),
    path('api/vehicles/locations/',                         views.api_vehicle_locations,          name='api_vehicle_locations'),
    path('api/vehicles/<str:vehicle_id>/location/',         views.api_update_vehicle_location,    name='api_update_vehicle_location'),
    path('api/vehicles/simulate/',                          views.api_simulate_vehicle_movement,  name='api_simulate_movement'),
    path('api/notifications/',                              views.api_notifications,              name='api_notifications'),
    path('api/notifications/mark-read/',                    views.api_mark_notifications_read,    name='api_mark_notifications_read'),
    path('api/analytics/',                                  views.api_analytics,                  name='api_analytics'),
]
