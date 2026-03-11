"""
URL patterns for Waste Management app
"""
from django.urls import path
from . import views

urlpatterns = [
    # ── Dashboard ────────────────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),

    # ── Vehicles ─────────────────────────────────────────────────────
    path('vehicles/',                       views.vehicles_list,   name='vehicles_list'),
    path('vehicles/edit/<str:vehicle_id>/', views.vehicle_update,  name='vehicle_update'),
    path('vehicles/delete/<str:vehicle_id>/', views.vehicle_delete, name='vehicle_delete'),

    # ── Routes ───────────────────────────────────────────────────────
    path('routes/',                       views.routes_list,   name='routes_list'),
    path('routes/edit/<str:route_id>/',   views.route_update,  name='route_update'),
    path('routes/delete/<str:route_id>/', views.route_delete,  name='route_delete'),

    # ── Schedules ────────────────────────────────────────────────────
    path('schedules/',                           views.schedules_list,   name='schedules_list'),
    path('schedules/edit/<str:schedule_id>/',    views.schedule_update,  name='schedule_update'),
    path('schedules/delete/<str:schedule_id>/',  views.schedule_delete,  name='schedule_delete'),

    # ── Map ──────────────────────────────────────────────────────────
    path('map/', views.map_view, name='map_view'),

    # ── JSON API ─────────────────────────────────────────────────────
    path('api/routes/', views.api_routes, name='api_routes'),
]
