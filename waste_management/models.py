"""
MongoEngine Document Models for Waste Collection Management System

Collections:
  - vehicles          → Vehicle
  - routes            → Route
  - schedules         → Schedule
  - waste_bins        → WasteBin          [NEW]
  - complaints        → Complaint         [NEW]
  - notifications     → Notification      [NEW]
  - waste_collections → WasteCollection   [NEW]
"""

import mongoengine as me
from datetime import datetime


# ─── PickupPoint Embedded Document ─────────────────────────────────────────────
class PickupPoint(me.EmbeddedDocument):
    """
    Represents a single GPS coordinate for a waste pickup location.
    Embedded inside Route documents as a list.
    """
    lat = me.FloatField(required=True)
    lng = me.FloatField(required=True)

    def to_dict(self):
        return {'lat': self.lat, 'lng': self.lng}


# ─── Vehicle Document ────────────────────────────────────────────────────────
class Vehicle(me.Document):
    """
    Represents a waste collection vehicle.
    MongoDB collection: vehicles
    """
    meta = {'collection': 'vehicles', 'ordering': ['vehicle_id']}

    vehicle_id   = me.StringField(required=True, unique=True, max_length=20)
    driver_name  = me.StringField(required=True, max_length=100)
    capacity     = me.StringField(required=True, max_length=50)
    status       = me.StringField(
        required=True,
        choices=['Active', 'Inactive', 'Under Maintenance'],
        default='Active'
    )
    # Live tracking fields
    current_lat  = me.FloatField(default=13.0827)   # Default: Chennai center
    current_lng  = me.FloatField(default=80.2707)
    waste_type   = me.StringField(
        choices=['General', 'Organic', 'Plastic', 'Metal', 'Mixed'],
        default='Mixed'
    )
    last_location_update = me.DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':            str(self.id),
            'vehicle_id':    self.vehicle_id,
            'driver_name':   self.driver_name,
            'capacity':      self.capacity,
            'status':        self.status,
            'current_lat':   self.current_lat,
            'current_lng':   self.current_lng,
            'waste_type':    self.waste_type,
            'last_updated':  self.last_location_update.isoformat() if self.last_location_update else None,
        }

    def __str__(self):
        return f"{self.vehicle_id} – {self.driver_name}"


# ─── Route Document ──────────────────────────────────────────────────────────
class Route(me.Document):
    """
    Represents a waste collection route covering an area with multiple pickup points.
    MongoDB collection: routes
    """
    meta = {'collection': 'routes', 'ordering': ['route_id']}

    route_id      = me.StringField(required=True, unique=True, max_length=20)
    area          = me.StringField(required=True, max_length=100)
    pickup_points = me.EmbeddedDocumentListField(PickupPoint)

    def to_dict(self):
        return {
            'id':            str(self.id),
            'route_id':      self.route_id,
            'area':          self.area,
            'pickup_points': [p.to_dict() for p in self.pickup_points],
        }

    def __str__(self):
        return f"{self.route_id} – {self.area}"


# ─── Schedule Document ────────────────────────────────────────────────────────
class Schedule(me.Document):
    """
    Represents a scheduled waste collection job.
    MongoDB collection: schedules
    """
    meta = {'collection': 'schedules', 'ordering': ['-collection_date']}

    schedule_id     = me.StringField(required=True, unique=True, max_length=20)
    vehicle_id      = me.StringField(required=True, max_length=20)
    route_id        = me.StringField(required=True, max_length=20)
    collection_date = me.StringField(required=True, max_length=10)
    status          = me.StringField(
        required=True,
        choices=['Pending', 'In Progress', 'Completed', 'Cancelled'],
        default='Pending'
    )

    def to_dict(self):
        return {
            'id':              str(self.id),
            'schedule_id':     self.schedule_id,
            'vehicle_id':      self.vehicle_id,
            'route_id':        self.route_id,
            'collection_date': self.collection_date,
            'status':          self.status,
        }

    def __str__(self):
        return f"{self.schedule_id} – {self.vehicle_id} on {self.collection_date}"


# ─── WasteBin Document ────────────────────────────────────────────────────────
class WasteBin(me.Document):
    """
    Represents a smart waste bin with fill-level monitoring.
    MongoDB collection: waste_bins
    """
    meta = {'collection': 'waste_bins', 'ordering': ['bin_id']}

    bin_id       = me.StringField(required=True, unique=True, max_length=20)
    area         = me.StringField(required=True, max_length=100)
    lat          = me.FloatField(required=True)
    lng          = me.FloatField(required=True)
    fill_level   = me.IntField(default=0, min_value=0, max_value=100)  # 0–100%
    waste_type   = me.StringField(
        choices=['General', 'Organic', 'Plastic', 'Metal'],
        default='General'
    )
    last_updated = me.DateTimeField(default=datetime.utcnow)

    @property
    def status(self):
        if self.fill_level >= 80:
            return 'Full'
        elif self.fill_level >= 50:
            return 'Half'
        else:
            return 'Low'

    @property
    def color(self):
        if self.fill_level >= 80:
            return 'red'
        elif self.fill_level >= 50:
            return 'yellow'
        return 'green'

    def to_dict(self):
        return {
            'id':          str(self.id),
            'bin_id':      self.bin_id,
            'area':        self.area,
            'lat':         self.lat,
            'lng':         self.lng,
            'fill_level':  self.fill_level,
            'waste_type':  self.waste_type,
            'status':      self.status,
            'color':       self.color,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }

    def __str__(self):
        return f"{self.bin_id} – {self.area} ({self.fill_level}%)"


# ─── Complaint Document ───────────────────────────────────────────────────────
class Complaint(me.Document):
    """
    Citizen complaint about waste issues.
    MongoDB collection: complaints
    """
    meta = {'collection': 'complaints', 'ordering': ['-created_at']}

    CATEGORIES = ['Overflowing Bin', 'Missed Pickup', 'Illegal Dumping', 'Other']
    STATUSES   = ['Open', 'Under Review', 'Resolved', 'Closed']

    complaint_id = me.StringField(required=True, unique=True, max_length=20)
    category     = me.StringField(required=True, choices=CATEGORIES)
    description  = me.StringField(required=True, max_length=1000)
    image_path   = me.StringField(default='')          # Relative path to uploaded image
    lat          = me.FloatField(default=13.0827)
    lng          = me.FloatField(default=80.2707)
    address      = me.StringField(default='', max_length=200)
    reporter_name = me.StringField(default='Anonymous', max_length=100)
    status       = me.StringField(choices=STATUSES, default='Open')
    admin_note   = me.StringField(default='', max_length=500)
    created_at   = me.DateTimeField(default=datetime.utcnow)
    resolved_at  = me.DateTimeField()

    def to_dict(self):
        return {
            'id':            str(self.id),
            'complaint_id':  self.complaint_id,
            'category':      self.category,
            'description':   self.description,
            'image_path':    self.image_path,
            'lat':           self.lat,
            'lng':           self.lng,
            'address':       self.address,
            'reporter_name': self.reporter_name,
            'status':        self.status,
            'admin_note':    self.admin_note,
            'created_at':    self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'resolved_at':   self.resolved_at.strftime('%Y-%m-%d %H:%M') if self.resolved_at else '',
        }

    def __str__(self):
        return f"{self.complaint_id} – {self.category} ({self.status})"


# ─── Notification Document ────────────────────────────────────────────────────
class Notification(me.Document):
    """
    System alert / notification.
    MongoDB collection: notifications
    """
    meta = {'collection': 'notifications', 'ordering': ['-created_at']}

    TYPES = ['info', 'warning', 'error', 'success']

    title      = me.StringField(required=True, max_length=200)
    message    = me.StringField(required=True, max_length=500)
    notif_type = me.StringField(choices=TYPES, default='info')
    is_read    = me.BooleanField(default=False)
    created_at = me.DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':         str(self.id),
            'title':      self.title,
            'message':    self.message,
            'type':       self.notif_type,
            'is_read':    self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
        }


# ─── WasteCollection Document ─────────────────────────────────────────────────
class WasteCollection(me.Document):
    """
    Records of actual waste collected per area per day.
    Used for analytics / Chart.js charts.
    MongoDB collection: waste_collections
    """
    meta = {'collection': 'waste_collections', 'ordering': ['-date']}

    area            = me.StringField(required=True, max_length=100)
    date            = me.StringField(required=True, max_length=10)   # YYYY-MM-DD
    tonnes_collected = me.FloatField(default=0.0)
    waste_type      = me.StringField(
        choices=['General', 'Organic', 'Plastic', 'Metal', 'Mixed'],
        default='Mixed'
    )
    vehicle_id      = me.StringField(default='', max_length=20)

    def to_dict(self):
        return {
            'id':               str(self.id),
            'area':             self.area,
            'date':             self.date,
            'tonnes_collected': self.tonnes_collected,
            'waste_type':       self.waste_type,
            'vehicle_id':       self.vehicle_id,
        }
