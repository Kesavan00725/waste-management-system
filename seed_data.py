"""
Seed script for Waste Collection Management System
Populates MongoDB with sample data for ALL collections:
  - vehicles, routes, schedules (original)
  - waste_bins, complaints, notifications, waste_collections (new)

Run: python seed_data.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_collection_project.settings')

import django
django.setup()

import mongoengine as me
from waste_collection_project.settings import MONGODB_SETTINGS
me.connect(**MONGODB_SETTINGS)

from waste_management.models import (
    Vehicle, Route, Schedule, PickupPoint,
    WasteBin, Complaint, Notification, WasteCollection, User
)
from datetime import datetime, timedelta


def clear_all():
    print("🗑  Clearing existing data...")
    Vehicle.objects.all().delete()
    Route.objects.all().delete()
    Schedule.objects.all().delete()
    WasteBin.objects.all().delete()
    Complaint.objects.all().delete()
    Notification.objects.all().delete()
    WasteCollection.objects.all().delete()
    User.objects.all().delete()

def seed_users():
    print("👤  Seeding users...")
    users_data = [
        ('Admin', 'Admin User', 'admin@wastetrack.com', 'admin123', '9876543210'),
        ('Citizen', 'John Doe', 'citizen@example.com', 'citizen123', '1234567890'),
        ('Citizen', 'Priya Rajan', 'priya@example.com', 'citizen123', '9876123450'),
        ('Citizen', 'Rahul Sharma', 'rahul.s@example.com', 'citizen123', '9988776655'),
        ('Citizen', 'Kavitha Iyer', 'kavitha.i@example.com', 'citizen123', '9123456780'),
        ('Citizen', 'Vijay Kumar', 'vijay.k@example.com', 'citizen123', '9845123670'),
        ('Citizen', 'Anita Desai', 'anita.d@example.com', 'citizen123', '8765432109'),
        ('Citizen', 'Suresh Babu', 'suresh.b@example.com', 'citizen123', '9012345678'),
        ('Citizen', 'Deepa Nair', 'deepa.n@example.com', 'citizen123', '8901234567'),
        ('Citizen', 'Arjun Reddy', 'arjun.r@example.com', 'citizen123', '7890123456'),
        ('Citizen', 'Lakshmi P', 'lakshmi.p@example.com', 'citizen123', '8123456789'),
        ('Citizen', 'Karthik S', 'karthik.s@example.com', 'citizen123', '9234567890'),
        ('Citizen', 'Meenakshi N', 'meena.n@example.com', 'citizen123', '8345678901'),
        ('Citizen', 'Ramakrishnan', 'ram.k@example.com', 'citizen123', '9456789012'),
        ('Citizen', 'Divya R', 'divya.r@example.com', 'citizen123', '8567890123'),
        ('Citizen', 'Sanjay M', 'sanjay.m@example.com', 'citizen123', '9678901234'),
        ('Citizen', 'Pooja V', 'pooja.v@example.com', 'citizen123', '8789012345'),
        ('Citizen', 'Murali K', 'murali.k@example.com', 'citizen123', '9890123456'),
        ('Citizen', 'Shweta B', 'shweta.b@example.com', 'citizen123', '8990123456'),
        ('Citizen', 'Varun T', 'varun.t@example.com', 'citizen123', '9090123456'),
        ('Citizen', 'Nithya G', 'nithya.g@example.com', 'citizen123', '8190123456'),
        ('Citizen', 'Ashwin D', 'ashwin.d@example.com', 'citizen123', '9290123456'),
    ]
    created_users = {}
    for role, name, email, pwd, phone in users_data:
        try:
            u = User(role=role, full_name=name, email=email, phone=phone)
            u.set_password(pwd)
            u.save()
            created_users[email] = str(u.id)
            print(f"   ✅ {role}: {email} (pw: {pwd})")
        except Exception as e:
            print(f"   ⚠️  {email}: {e}")
    return created_users


def seed_vehicles():
    print("🚛  Seeding vehicles...")
    vehicles = [
        Vehicle(vehicle_id='V101', driver_name='Arun Kumar',    capacity='2 Tons', status='Active',            waste_type='General', current_lat=13.0200, current_lng=80.2100),
        Vehicle(vehicle_id='V102', driver_name='Priya Rajan',   capacity='3 Tons', status='Active',            waste_type='Organic', current_lat=13.0500, current_lng=80.2400),
        Vehicle(vehicle_id='V103', driver_name='Karthik Nair',  capacity='2 Tons', status='Active',            waste_type='Plastic', current_lat=13.0800, current_lng=80.2700),
        Vehicle(vehicle_id='V104', driver_name='Meena Devi',    capacity='4 Tons', status='Inactive',          waste_type='Metal',   current_lat=13.0600, current_lng=80.2300),
        Vehicle(vehicle_id='V105', driver_name='Suresh Babu',   capacity='2 Tons', status='Under Maintenance', waste_type='Mixed',   current_lat=13.0400, current_lng=80.2600),
        Vehicle(vehicle_id='V106', driver_name='Divya Lakshmi', capacity='3 Tons', status='Active',            waste_type='Mixed',   current_lat=13.0700, current_lng=80.2500),
    ]
    for v in vehicles:
        try:
            v.save()
            print(f"   ✅ {v.vehicle_id} — {v.driver_name}")
        except Exception as e:
            print(f"   ⚠️  {v.vehicle_id}: {e}")


def seed_routes():
    print("🗺️  Seeding routes...")
    routes_data = [
        {
            'route_id': 'R201', 'area': 'Adyar',
            'points': [(13.0067, 80.2572), (13.0012, 80.2530), (13.0089, 80.2612), (13.0050, 80.2490)]
        },
        {
            'route_id': 'R202', 'area': 'T. Nagar',
            'points': [(13.0418, 80.2341), (13.0375, 80.2299), (13.0452, 80.2383), (13.0400, 80.2260)]
        },
        {
            'route_id': 'R203', 'area': 'Anna Nagar',
            'points': [(13.0850, 80.2101), (13.0900, 80.2150), (13.0820, 80.2070), (13.0870, 80.2200)]
        },
        {
            'route_id': 'R204', 'area': 'Velachery',
            'points': [(12.9815, 80.2180), (12.9770, 80.2140), (12.9845, 80.2220), (12.9790, 80.2100)]
        },
        {
            'route_id': 'R205', 'area': 'Mylapore',
            'points': [(13.0368, 80.2676), (13.0320, 80.2640), (13.0400, 80.2710), (13.0350, 80.2600)]
        },
    ]
    for rd in routes_data:
        try:
            route = Route(
                route_id=rd['route_id'],
                area=rd['area'],
                pickup_points=[PickupPoint(lat=lat, lng=lng) for lat, lng in rd['points']]
            )
            route.save()
            print(f"   ✅ {rd['route_id']} — {rd['area']} ({len(rd['points'])} points)")
        except Exception as e:
            print(f"   ⚠️  {rd['route_id']}: {e}")


def seed_schedules():
    print("📅  Seeding schedules...")
    today = datetime.now().date()
    schedules_data = [
        ('S501', 'V101', 'R201', str(today - timedelta(days=1)), 'Completed'),
        ('S502', 'V102', 'R202', str(today - timedelta(days=1)), 'Completed'),
        ('S503', 'V103', 'R203', str(today),                     'In Progress'),
        ('S504', 'V106', 'R204', str(today),                     'Pending'),
        ('S505', 'V101', 'R205', str(today + timedelta(days=1)), 'Pending'),
        ('S506', 'V102', 'R201', str(today + timedelta(days=2)), 'Pending'),
        ('S507', 'V103', 'R202', str(today - timedelta(days=2)), 'Completed'),
        ('S508', 'V106', 'R203', str(today - timedelta(days=3)), 'Completed'),
        ('S509', 'V101', 'R204', str(today - timedelta(days=3)), 'Cancelled'),
        ('S510', 'V102', 'R205', str(today - timedelta(days=4)), 'Completed'),
    ]
    for sid, vid, rid, date, status in schedules_data:
        try:
            Schedule(schedule_id=sid, vehicle_id=vid, route_id=rid,
                     collection_date=date, status=status).save()
            print(f"   ✅ {sid} — {vid}/{rid} → {status}")
        except Exception as e:
            print(f"   ⚠️  {sid}: {e}")


def seed_bins():
    print("🗑  Seeding waste bins...")
    bins_data = [
        # (bin_id, area, lat, lng, fill_level, waste_type)
        ('BIN001', 'Adyar',     13.0067, 80.2572,  85, 'General'),
        ('BIN002', 'Adyar',     13.0050, 80.2490,  42, 'Organic'),
        ('BIN003', 'T. Nagar',  13.0418, 80.2341,  92, 'General'),
        ('BIN004', 'T. Nagar',  13.0400, 80.2260,  55, 'Plastic'),
        ('BIN005', 'Anna Nagar',13.0850, 80.2101,  20, 'General'),
        ('BIN006', 'Anna Nagar',13.0870, 80.2200,  78, 'Organic'),
        ('BIN007', 'Velachery', 12.9815, 80.2180,  95, 'General'),
        ('BIN008', 'Velachery', 12.9790, 80.2100,  33, 'Plastic'),
        ('BIN009', 'Mylapore',  13.0368, 80.2676,  60, 'Metal'),
        ('BIN010', 'Mylapore',  13.0350, 80.2600,  15, 'General'),
        ('BIN011', 'Guindy',    13.0067, 80.2153,  88, 'Organic'),
        ('BIN012', 'Nungambakkam', 13.0569, 80.2425, 45, 'General'),
    ]
    for bin_id, area, lat, lng, fill, wtype in bins_data:
        try:
            WasteBin(bin_id=bin_id, area=area, lat=lat, lng=lng,
                     fill_level=fill, waste_type=wtype).save()
            icon = '🔴' if fill >= 80 else ('🟡' if fill >= 50 else '🟢')
            print(f"   {icon} {bin_id} — {area} → {fill}%")
        except Exception as e:
            print(f"   ⚠️  {bin_id}: {e}")


def seed_complaints(users_dict):
    print("📢  Seeding complaints...")
    
    # Get IDs of our seeded citizens
    john_id = users_dict.get('citizen@example.com', '')
    priya_id = users_dict.get('priya@example.com', '')

    complaints_data = [
        ('C001', 'Overflowing Bin',  'Bin at Adyar beach road is overflowing since 2 days.',           13.0067, 80.2572, 'Adyar Beach Road', 'John Doe',   john_id, 'Open'),
        ('C002', 'Missed Pickup',    'Our street was skipped during yesterday\'s collection.',          13.0418, 80.2341, 'Mahalingapuram',   'Priya S',    priya_id, 'Under Review'),
        ('C003', 'Illegal Dumping',  'Large pile of construction debris dumped near the park.',         12.9815, 80.2180, 'Velachery Main Rd','Kavi Arasu', '',       'Open'),
        ('C004', 'Overflowing Bin',  'Bin near T.Nagar bus stand is full and smelling bad.',           13.0375, 80.2299, 'T Nagar Bus Stand','John Doe',   john_id,  'Resolved'),
        ('C005', 'Other',            'Waste water from the bin is flowing into the road.',              13.0850, 80.2101, 'Anna Nagar 5th St','Priya S',    priya_id, 'Closed'),
    ]
    for cid, cat, desc, lat, lng, addr, reporter, user_id, status in complaints_data:
        try:
            c = Complaint(
                complaint_id=cid, category=cat, description=desc,
                lat=lat, lng=lng, address=addr, reporter_name=reporter, 
                user_id=user_id, status=status,
                created_at=datetime.utcnow() - timedelta(days=len(cid)),
            )
            if status in ('Resolved', 'Closed'):
                c.resolved_at = datetime.utcnow() - timedelta(hours=12)
                c.admin_note = 'Issue investigated and resolved. Bin cleared and cleaned.'
            c.save()
            print(f"   ✅ {cid} — {cat} [{status}]")
        except Exception as e:
            print(f"   ⚠️  {cid}: {e}")


def seed_notifications():
    print("🔔  Seeding notifications...")
    notifs = [
        ('Full Bin Alert',              'BIN007 in Velachery is at 95% capacity. Schedule immediate collection.',  'error',   False),
        ('Full Bin Alert',              'BIN003 in T. Nagar is at 92% capacity. Needs attention.',                 'error',   False),
        ('Scheduled Pickup Completed',  'Schedule S507 for Route R202 completed successfully.',                    'success', True),
        ('New Complaint Received',      'Complaint #C003: Illegal Dumping reported by Kavi Arasu.',                'warning', False),
        ('Vehicle Under Maintenance',   'V105 (Suresh Babu) is now marked as Under Maintenance.',                  'warning', True),
        ('Pickup Missed',               'Schedule S509 for Route R204 was cancelled. Reschedule required.',        'error',   False),
        ('System Online',               'WasteTrack Smart City system started successfully.',                       'info',    True),
    ]
    for i, (title, msg, ntype, is_read) in enumerate(notifs):
        try:
            Notification(
                title=title, message=msg, notif_type=ntype, is_read=is_read,
                created_at=datetime.utcnow() - timedelta(hours=i * 3)
            ).save()
            icon = '✅' if is_read else '🔴'
            print(f"   {icon} [{ntype.upper()}] {title}")
        except Exception as e:
            print(f"   ⚠️  {title}: {e}")


def seed_waste_collections():
    print("📊  Seeding waste collection records (for analytics)...")
    areas = ['Adyar', 'T. Nagar', 'Anna Nagar', 'Velachery', 'Mylapore', 'Guindy', 'Nungambakkam', 'Porur']
    waste_types = ['General', 'Organic', 'Plastic', 'Metal', 'Mixed']
    vehicles = ['V101', 'V102', 'V103', 'V106']
    today = datetime.now().date()
    records = []
    # Generate 30 days of data
    for i in range(30):
        day = today - timedelta(days=i)
        day_str = str(day)
        # 2-4 collections per day
        for j in range(3):
            area = areas[(i + j) % len(areas)]
            wtype = waste_types[(i + j) % len(waste_types)]
            vehicle = vehicles[j % len(vehicles)]
            tonnes = round(0.5 + (i % 5) * 0.3 + j * 0.2, 2)
            records.append(WasteCollection(
                area=area, date=day_str, tonnes_collected=tonnes,
                waste_type=wtype, vehicle_id=vehicle
            ))
    try:
        WasteCollection.objects.insert(records)
        print(f"   ✅ {len(records)} waste collection records inserted")
    except Exception as e:
        print(f"   ⚠️  Batch insert failed, trying one by one: {e}")
        for r in records:
            try:
                r.save()
            except Exception:
                pass
        print(f"   ✅ Done")


if __name__ == '__main__':
    print("\n════════════════════════════════════════════════════")
    print("  WasteTrack Smart City — Database Seed Script")
    print("════════════════════════════════════════════════════\n")

    clear_all()
    users_dict = seed_users()
    seed_vehicles()
    seed_routes()
    seed_schedules()
    seed_bins()
    seed_complaints(users_dict)
    seed_notifications()
    seed_waste_collections()

    print("\n════════════════════════════════════════════════════")
    print("  ✅  All data seeded successfully!")
    print(f"  👤  Users:       {User.objects.count()}")
    print(f"  🚛  Vehicles:    {Vehicle.objects.count()}")
    print(f"  🗺️  Routes:      {Route.objects.count()}")
    print(f"  📅  Schedules:   {Schedule.objects.count()}")
    print(f"  🗑  Bins:        {WasteBin.objects.count()}")
    print(f"  📢  Complaints:  {Complaint.objects.count()}")
    print(f"  🔔  Notifs:      {Notification.objects.count()}")
    print(f"  📊  Collections: {WasteCollection.objects.count()}")
    print("════════════════════════════════════════════════════\n")
