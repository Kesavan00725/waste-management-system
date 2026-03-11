"""
MongoEngine Document Models for Waste Collection Management System

These documents map directly to MongoDB collections:
  - Vehicle      → vehicles collection
  - Route        → routes collection
  - Schedule     → schedules collection
"""

import mongoengine as me


# ─── PickupPoint Embedded Document ─────────────────────────────────────────────
class PickupPoint(me.EmbeddedDocument):
    """
    Represents a single GPS coordinate for a waste pickup location.
    Embedded inside Route documents as a list.
    """
    lat = me.FloatField(required=True)   # Latitude  (e.g. 13.0067)
    lng = me.FloatField(required=True)   # Longitude (e.g. 80.2572)

    def to_dict(self):
        return {'lat': self.lat, 'lng': self.lng}


# ─── Vehicle Document ────────────────────────────────────────────────────────
class Vehicle(me.Document):
    """
    Represents a waste collection vehicle.
    MongoDB collection: vehicles
    Example: { vehicle_id: "V101", driver_name: "Arun", capacity: "2 Tons", status: "Active" }
    """
    meta = {'collection': 'vehicles', 'ordering': ['vehicle_id']}

    vehicle_id   = me.StringField(required=True, unique=True, max_length=20)
    driver_name  = me.StringField(required=True, max_length=100)
    capacity     = me.StringField(required=True, max_length=50)   # e.g. "2 Tons"
    status       = me.StringField(
        required=True,
        choices=['Active', 'Inactive', 'Under Maintenance'],
        default='Active'
    )

    def to_dict(self):
        return {
            'id': str(self.id),
            'vehicle_id':  self.vehicle_id,
            'driver_name': self.driver_name,
            'capacity':    self.capacity,
            'status':      self.status,
        }

    def __str__(self):
        return f"{self.vehicle_id} – {self.driver_name}"


# ─── Route Document ──────────────────────────────────────────────────────────
class Route(me.Document):
    """
    Represents a waste collection route covering an area with multiple pickup points.
    MongoDB collection: routes
    Example: { route_id: "R201", area: "Adyar", pickup_points: [{lat:13.0067, lng:80.2572}, ...] }
    """
    meta = {'collection': 'routes', 'ordering': ['route_id']}

    route_id      = me.StringField(required=True, unique=True, max_length=20)
    area          = me.StringField(required=True, max_length=100)
    pickup_points = me.EmbeddedDocumentListField(PickupPoint)   # List of lat/lng points

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
    Links a Vehicle to a Route on a specific date.
    MongoDB collection: schedules
    Example: { schedule_id: "S501", vehicle_id: "V101", route_id: "R201",
               collection_date: "2026-03-15", status: "Pending" }
    """
    meta = {'collection': 'schedules', 'ordering': ['-collection_date']}

    schedule_id     = me.StringField(required=True, unique=True, max_length=20)
    vehicle_id      = me.StringField(required=True, max_length=20)   # References Vehicle.vehicle_id
    route_id        = me.StringField(required=True, max_length=20)   # References Route.route_id
    collection_date = me.StringField(required=True, max_length=10)   # "YYYY-MM-DD"
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
