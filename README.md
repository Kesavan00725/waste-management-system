# ♻️ WasteTrack Smart City: Waste Collection Scheduling Management System

A full-stack, enterprise-grade Django + MongoDB web application designed to help municipalities manage waste collection vehicles, routes, schedules, and citizen interactions. Featuring a modern dual-pane authentication UI, role-based access control, live Google Maps visualization, smart bin monitoring, data analytics, and Excel exports.

---

## ✨ Smart City Features

1. **Role-Based Portals & Authentication**: Complete segregation between **Administrators** (full municipal control) and **Citizens** (complaint tracking) with secure, custom Werkzeug hashed passwords and file-based session management.
2. **Premium Dual-Pane UI**: The login and registration flows feature stunning, photo-realistic generated backgrounds and smooth glass-morphism effects seamlessly integrated with Bootstrap 5.3.
3. **Advanced Dashboard Analytics**: Interactive Chart.js visualizations showing waste collected per area, daily pickup statistics, vehicle usage, and real-time bin fill levels.
4. **Live Vehicle Tracking**: Real-time simulated vehicle movement on the map with GPS coordinates updated on a polling interval.
5. **Smart Waste Bin Monitoring**: Real-time tracking of waste bin fill levels (0–100%). Bins are logically color-coded (red, yellow, green) based on status on the map and dashboard.
6. **Citizen Complaint Portal**: A dedicated public portal for authenticated citizens to report overflowing bins, missed pickups, or illegal dumping via map coordinates and images. Integrated with unique User IDs.
7. **Citizen Data Export (Admin)**: The administration panel includes a dedicated 'Citizens' roster with direct one-click **Excel / CSV** database exporting capabilities.
8. **Notification System**: Real-time alerts for system events, full bins, assigned complaints, and scheduled collections with an unread badge indicator.
9. **Advanced Map Visualization**: A centralized Google Maps view combining vehicle live tracking, bin locations, route overlays, and a dynamic Heatmap layer showing high-waste generation areas.

---

## 📁 Project Structure

```
waste_collection_project/
├── manage.py
├── requirements.txt
├── README.md
├── seed_data.py                    ← Script to populate database with 20+ realistic profiles, vehicles, bins & generated data
│
├── waste_collection_project/       ← Django project package
│   ├── settings.py                 ← MongoDB config, API keys, Media & File-based Session routes
│   └── urls.py                     ← Root URLs and Media serving
│
├── waste_management/               ← Main app
│   ├── auth.py                     ← Secure role-based access decorators (@require_admin, etc.)
│   ├── models.py                   ← MongoEngine documents (Users, Vehicles, Bins, Complaints, etc.)
│   ├── views.py                    ← CRUD logic & API endpoints for async map/chart updates
│   └── urls.py                     ← App URL setup
│
├── templates/                      ← Django HTML templates (Bootstrap 5)
│   ├── base.html                   ← Main layout with dynamic sidebar rendering based on User Role
│   ├── login.html                  ← Advanced dual-pane hero image authentication UI
│   ├── register.html               ← Registration flow UI
│   ├── dashboard.html              ← Admin Overview stats and recent activity
│   ├── citizen_dashboard.html      ← Citizen-specific portal
│   ├── map.html                    ← Live tracking & heatmap
│   ├── bins.html                   ← Smart Bin monitoring
│   ├── citizens.html               ← Admin view of registered citizens & Excel export
│   ├── complaints.html             ← Admin global complaint listing
│   ├── citizen_complaints.html     ← Citizen-specific mapped complaint history
│   └── ... (analytics, notifications, vehicles, routes, schedules)
│
├── media/                          ← User uploaded files (Complaint images)
└── static/
    ├── css/style.css               ← Professional Municipal Theme + Animations
    ├── js/script.js                ← Base UI interactive logic
    └── images/                     ← UI generated branding imagery
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
> *Tip for DB Management:* We recommend installing **MongoDB Compass** to visually manage and verify your local database tables.

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
# Ensure mongoengine, pymongo, and werkzeug are installed!
```

### 6. Configure Google Maps API Key
Open `waste_collection_project/settings.py` and replace:
```python
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY_HERE'
```
with your actual key.

### 7. Seed the Database (Important)
We provide a comprehensive data seeder to immediately populate the system with Admin models, Citizens, vehicles, routes, bins, complaints, notifications, and analytics data.
```bash
python seed_data.py
```
*Note: The seeder provisions the default admin context (`admin@wastetrack.com` / `admin123`).*

### 8. Run the development server
```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

---

## 🗄️ MongoDB Architecture (MongoEngine)

The app utilizes Django for routing, session management, and templating. Database operations (including User Auth and password validation) are handled strictly via **MongoEngine** interacting directly with NoSQL documents. Django's built-in SQL ORM is bypassed.

Key collections:
- `users` (New): Handles Administrators and registered Citizens with Werkzeug password hashing.
- `vehicles`: Includes capacities, driver specs, waste_type, and current GPS coordinates.
- `routes`: Includes list of embedded lat/lng pickup point documents.
- `schedules`: Joins vehicles and routes with collection dates.
- `waste_bins`: Includes lat/lng, threshold levels (0-100%), and waste types.
- `complaints`: Stores citizen-reported issues, image paths, coordinates, admin notes, and relational User IDs.
- `notifications`: System alerts and logical tracking statuses.
- `waste_collections`: Historical ledger of collected waste (in tonnes) used for reporting analytics.

---

## 🌐 API & Integration points

The web frontend communicates dynamically with the Django backend via dedicated JSON API routes:
- `POST /api/vehicles/simulate/`: Progresses vehicle movement along route paths for the live map simulation.
- `GET /api/vehicles/locations/`: Fetches immediate vehicle coordinates for the local map tracking polling.
- `GET /api/bins/`: Returns current statuses of all sensor-equipped bins.
- `GET /api/analytics/`: Compiles real-time aggregations from historical collections, bin data, and vehicle fleets for Chart.js.
- `GET /citizens/export/`: Generates and downloads pure CSV/Excel streams natively from MongoDB.