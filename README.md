# ♻️ WasteTrack Smart City: Waste Collection Scheduling Management System

A full-stack Django + MongoDB web application to help municipalities manage waste collection vehicles, routes, schedules, and citizen interactions — featuring a modern dashboard, live Google Maps visualization, smart bin monitoring, and data analytics.

---

## ✨ Smart City Features

1. **Dashboard Analytics**: Interactive Chart.js visualizations showing waste collected per area, daily pickup statistics, vehicle usage, and bin fill levels.
2. **Live Vehicle Tracking**: Real-time simulated vehicle movement on the map with GPS coordinates updated on a polling interval.
3. **Smart Waste Bin Monitoring**: Real-time tracking of waste bin fill levels (0–100%). Bins are color-coded (red, yellow, green) based on their status on the map and dashboard.
4. **Citizen Complaint System**: Public portal for citizens to report overflowing bins, missed pickups, or illegal dumping. Supports image uploads, map-based location tagging, and an admin interface for resolution tracking.
5. **Notification System**: Real-time alerts for system events, full bins, assigned complaints, and scheduled collections with an unread badge indicator.
6. **Advanced Map Visualization**: A centralized Google Maps view combining vehicle live tracking, bin locations, route overlays, and a dynamic Heatmap layer showing high-waste generation areas.
7. **Premium Municipal UI**: Fully responsive, clean, and professional light-themed interface built with Bootstrap 5.

---

## 📁 Project Structure

```
waste_collection_project/
├── manage.py
├── requirements.txt
├── README.md
├── seed_data.py                    ← Script to populate database with sample data
│
├── waste_collection_project/       ← Django project package
│   ├── settings.py                 ← MongoDB config, API keys, Media routes
│   └── urls.py                     ← Root URLs and Media serving
│
├── waste_management/               ← Main app
│   ├── models.py                   ← MongoEngine documents (Vehicles, Bins, Complaints, etc.)
│   ├── views.py                    ← CRUD logic & API endpoints for async map/chart updates
│   └── urls.py                     ← App URL setup
│
├── templates/                      ← Django HTML templates (Bootstrap 5)
│   ├── base.html                   ← Main layout with sidebar and topbar
│   ├── dashboard.html              ← Overview stats and recent activity
│   ├── analytics.html              ← Full page Chart.js analytics
│   ├── map.html                    ← Live tracking & heatmap
│   ├── bins.html                   ← Smart Bin monitoring
│   ├── complaints.html             ← Citizen complaint submission & listing
│   ├── complaint_detail.html       ← Admin resolution page for complaints
│   ├── notifications.html          ← Alert feed
│   └── ... (vehicles, routes, schedules CRUD templates)
│
├── media/                          ← User uploaded files (Complaint images)
└── static/
    ├── css/style.css               ← Professional Municipal Dashboard Theme
    └── js/script.js                ← Base UI interactive logic
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.10+
- MongoDB 6.0+ running on `localhost:27017`
- A Google Maps JavaScript API key (with Maps JS API enabled)

### 2. Install MongoDB
```bash
# macOS (Homebrew)
brew tap mongodb/brew && brew install mongodb-community
brew services start mongodb-community

# Ubuntu / Debian
sudo apt-get install -y mongodb
sudo systemctl start mongodb

# Windows — download installer from https://www.mongodb.com/try/download/community
```

### 3. Clone / Copy the project
```bash
cd waste_collection_project
```

### 4. Create a virtual environment
```bash
python -m venv venv

# Activate:
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 5. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 6. Configure Google Maps API Key
Open `waste_collection_project/settings.py` and replace:
```python
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY_HERE'
```
with your actual key.

> To get a free API key: https://developers.google.com/maps/documentation/javascript/get-api-key
> Enable: **Maps JavaScript API** in your Google Cloud project.

### 7. Seed the Database (Important)
We provide a comprehensive data seeder to immediately populate the system with vehicles, routes, bins, complaints, notifications, and analytics data.
```bash
python seed_data.py
```

### 8. Run the development server
```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

---

## 🗄️ MongoDB Collections (MongoEngine)

The app utilizes Django exclusively for routing, templating, and request handling. Database operations are handled purely via **MongoEngine** interacting directly with MongoDB. Django's built-in ORM is disabled (`DATABASES = {'default': {'ENGINE': 'django.db.backends.dummy'}}`).

Key collections:
- `vehicles`: Includes capacities, driver specs, waste_type, and current GPS coordinates.
- `routes`: Includes list of embedded lat/lng pickup point documents.
- `schedules`: Joins vehicles and routes with collection dates.
- `waste_bins`: Includes lat/lng, threshold levels (0-100%), and waste types.
- `complaints`: Stores citizen reports, image file paths, assigned coordinates, and admin notes.
- `notifications`: Stores system alerts and statuses.
- `waste_collections`: Historical ledger of collected waste (in tonnes) used for reporting analytics.

---

## 🌐 API & Integration points

The web frontend communicates dynamically with the Django backend via dedicated JSON API routes:
- `POST /api/vehicles/simulate/`: Progresses vehicle movement along route paths for the live map simulation.
- `GET /api/vehicles/locations/`: Fetches immediate vehicle coordinates for the map tracking polling.
- `GET /api/bins/`: Returns current statuses of all sensor-equipped bins.
- `GET /api/analytics/`: Compiles real-time aggregations from historical collections, bin data, and vehicle fleets for Chart.js.
- `GET /api/notifications/`: Polls notification unread counts.