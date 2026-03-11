#!/usr/bin/env python
"""
Seed script - Populates MongoDB with sample Chennai data.
Run: python seed_data.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_collection_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

# Wait for __init__.py to connect to MongoDB, then import models
from waste_management.models import Vehicle, Route, Schedule, PickupPoint
from datetime import datetime

print("🌱 Seeding Waste Collection Database with Chennai data...\n")

# ---- Clear existing data ----
Vehicle.objects.delete()
Route.objects.delete()
Schedule.objects.delete()
print("🗑️  Cleared existing data.")

# ---- Vehicles ----
vehicles_data = [
    {"vehicle_id": "V101", "driver_name": "Arun Kumar",    "capacity": "2 Tons",  "status": "Active"},
    {"vehicle_id": "V102", "driver_name": "Ravi Shankar",  "capacity": "3 Tons",  "status": "Active"},
    {"vehicle_id": "V103", "driver_name": "Priya Devi",    "capacity": "1.5 Tons","status": "Active"},
    {"vehicle_id": "V104", "driver_name": "Senthil Raj",   "capacity": "4 Tons",  "status": "Under Maintenance"},
    {"vehicle_id": "V105", "driver_name": "Meena Kumari",  "capacity": "2 Tons",  "status": "Inactive"},
]

for vd in vehicles_data:
    v = Vehicle(**vd)
    v.save()
    print(f"  ✅ Vehicle: {v.vehicle_id} - {v.driver_name}")

# ---- Routes (Chennai areas with real coordinates) ----
routes_data = [
    {
        "route_id": "R201",
        "area": "Adyar",
        "description": "Covers Adyar main roads and side streets",
        "pickup_points": [
            {"lat": 13.0067, "lng": 80.2572, "address": "Adyar Bus Terminus"},
            {"lat": 13.0080, "lng": 80.2590, "address": "Gandhi Nagar Junction"},
            {"lat": 13.0050, "lng": 80.2560, "address": "Adyar Market"},
            {"lat": 13.0095, "lng": 80.2610, "address": "Kasturba Nagar"},
        ]
    },
    {
        "route_id": "R202",
        "area": "T. Nagar",
        "description": "T. Nagar commercial and residential zone",
        "pickup_points": [
            {"lat": 13.0418, "lng": 80.2341, "address": "Panagal Park"},
            {"lat": 13.0400, "lng": 80.2320, "address": "Usman Road"},
            {"lat": 13.0435, "lng": 80.2360, "address": "T. Nagar Bus Stand"},
            {"lat": 13.0450, "lng": 80.2380, "address": "Pondy Bazaar"},
        ]
    },
    {
        "route_id": "R203",
        "area": "Anna Nagar",
        "description": "Anna Nagar western sector",
        "pickup_points": [
            {"lat": 13.0850, "lng": 80.2101, "address": "Anna Nagar Tower"},
            {"lat": 13.0867, "lng": 80.2120, "address": "2nd Avenue Junction"},
            {"lat": 13.0880, "lng": 80.2145, "address": "Anna Nagar Market"},
        ]
    },
    {
        "route_id": "R204",
        "area": "Tambaram",
        "description": "Tambaram suburban zone",
        "pickup_points": [
            {"lat": 12.9249, "lng": 80.1000, "address": "Tambaram Railway Station"},
            {"lat": 12.9230, "lng": 80.1020, "address": "Tambaram Market"},
            {"lat": 12.9260, "lng": 80.0980, "address": "Mudichur Road"},
        ]
    },
]

for rd in routes_data:
    points = [PickupPoint(lat=p['lat'], lng=p['lng'])
              for p in rd['pickup_points']]
    r = Route(
        route_id=rd['route_id'],
        area=rd['area'],
        pickup_points=points
    )
    r.save()
    print(f"  ✅ Route: {r.route_id} - {r.area} ({len(points)} stops)")

# ---- Schedules ----
schedules_data = [
    {"schedule_id": "S501", "vehicle_id": "V101", "route_id": "R201",
     "collection_date": "2026-03-15", "status": "Completed",
     "notes": "Morning shift, completed on time"},
    {"schedule_id": "S502", "vehicle_id": "V102", "route_id": "R202",
     "collection_date": "2026-03-16", "status": "Pending",
     "notes": "Special collection - festival cleanup"},
    {"schedule_id": "S503", "vehicle_id": "V103", "route_id": "R203",
     "collection_date": "2026-03-17", "status": "In Progress",
     "notes": ""},
    {"schedule_id": "S504", "vehicle_id": "V101", "route_id": "R204",
     "collection_date": "2026-03-18", "status": "Pending",
     "notes": "Heavy rainfall expected, take extra caution"},
    {"schedule_id": "S505", "vehicle_id": "V102", "route_id": "R201",
     "collection_date": "2026-03-19", "status": "Pending",
     "notes": ""},
]

for sd in schedules_data:
    s = Schedule(
        schedule_id=sd['schedule_id'],
        vehicle_id=sd['vehicle_id'],
        route_id=sd['route_id'],
        collection_date=sd['collection_date'],
        status=sd['status']
    )
    s.save()
    print(f"  ✅ Schedule: {s.schedule_id} - {s.vehicle_id} → {s.route_id} [{s.status}]")

print(f"""
✨ Database seeded successfully!
   📊 {Vehicle.objects.count()} vehicles
   🗺️  {Route.objects.count()} routes  
   📅 {Schedule.objects.count()} schedules
""")
