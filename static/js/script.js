/**
 * Waste Collection Management System — Main JavaScript
 * Handles: pickup point management, map interactions, form helpers
 */

/* ══════════════════════════════════════════════════════════════════════════
   PICKUP POINTS MANAGER (used on Route Create / Edit pages)
   ══════════════════════════════════════════════════════════════════════════ */

let pickupPoints = [];         // Array of {lat, lng} objects
let miniMap      = null;       // Google Maps instance (mini map in form)
let miniMarkers  = [];         // Markers on mini map
let mapClickListener = null;   // Listener handle

/**
 * Initialize the mini map inside route form.
 * Called by Google Maps callback after API loads.
 */
function initMiniMap() {
  const mapEl = document.getElementById('mini-map');
  if (!mapEl) return;

  // Centre on Chennai
  miniMap = new google.maps.Map(mapEl, {
    center: { lat: 13.0827, lng: 80.2707 },
    zoom: 12,
    styles: darkMapStyles(),
    disableDefaultUI: false,
    zoomControl: true,
  });

  // Load existing points if editing
  const existingEl = document.getElementById('existing-points');
  if (existingEl) {
    try {
      pickupPoints = JSON.parse(existingEl.value) || [];
      renderMiniMarkers();
    } catch(e) { pickupPoints = []; }
  }

  // Add point on map click
  mapClickListener = miniMap.addListener('click', (e) => {
    const point = { lat: e.latLng.lat(), lng: e.latLng.lng() };
    pickupPoints.push(point);
    renderMiniMarkers();
    syncPickupList();
  });
}

/** Re-draw all markers on mini map */
function renderMiniMarkers() {
  // Clear old markers
  miniMarkers.forEach(m => m.setMap(null));
  miniMarkers = [];

  pickupPoints.forEach((pt, i) => {
    const marker = new google.maps.Marker({
      position: pt,
      map: miniMap,
      title: `Point ${i + 1}`,
      label: { text: String(i + 1), color: '#0d1117', fontWeight: 'bold', fontSize: '11px' },
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 14,
        fillColor: '#39d353',
        fillOpacity: 1,
        strokeColor: '#0d1117',
        strokeWeight: 2,
      },
    });
    miniMarkers.push(marker);
  });

  // Update hidden input
  const hiddenInput = document.getElementById('pickup-points-json');
  if (hiddenInput) hiddenInput.value = JSON.stringify(pickupPoints);
}

/** Rebuild the pickup points list UI */
function syncPickupList() {
  const listEl = document.getElementById('pickup-list');
  if (!listEl) return;
  listEl.innerHTML = '';

  if (pickupPoints.length === 0) {
    listEl.innerHTML = '<p style="color:var(--text-muted);font-size:12px;">Click on the map to add pickup points.</p>';
    return;
  }

  pickupPoints.forEach((pt, i) => {
    const item = document.createElement('div');
    item.className = 'pickup-item';
    item.innerHTML = `
      <span>📍 <strong>Pt ${i + 1}</strong>&nbsp;&nbsp;${pt.lat.toFixed(5)}, ${pt.lng.toFixed(5)}</span>
      <button type="button" onclick="removePoint(${i})" title="Remove">✕</button>
    `;
    listEl.appendChild(item);
  });

  renderMiniMarkers();
}

/** Remove a pickup point by index */
function removePoint(index) {
  pickupPoints.splice(index, 1);
  syncPickupList();
  renderMiniMarkers();
}


/* ══════════════════════════════════════════════════════════════════════════
   FULL MAP VIEW (map.html)
   ══════════════════════════════════════════════════════════════════════════ */

let fullMap    = null;
let allMarkers = [];
let routeLines = [];

/**
 * Initialize the full-page map showing all routes.
 * routesData is injected by Django template as a global variable.
 */
function initFullMap() {
  const mapEl = document.getElementById('map-container');
  if (!mapEl || typeof routesData === 'undefined') return;

  fullMap = new google.maps.Map(mapEl, {
    center: { lat: 13.0827, lng: 80.2707 },   // Chennai
    zoom: 12,
    styles: darkMapStyles(),
  });

  const colors = ['#39d353', '#58a6ff', '#e3b341', '#f85149', '#d2a8ff', '#ffa657'];

  routesData.forEach((route, ri) => {
    const color = colors[ri % colors.length];
    const pts   = route.pickup_points || [];

    if (pts.length === 0) return;

    // Draw polyline connecting all pickup points
    const path = pts.map(p => ({ lat: p.lat, lng: p.lng }));
    const line = new google.maps.Polyline({
      path,
      geodesic: true,
      strokeColor: color,
      strokeOpacity: 0.85,
      strokeWeight: 3,
    });
    line.setMap(fullMap);
    routeLines.push(line);

    // Add markers for each pickup point
    pts.forEach((pt, pi) => {
      const marker = new google.maps.Marker({
        position: { lat: pt.lat, lng: pt.lng },
        map: fullMap,
        title: `${route.area} – Stop ${pi + 1}`,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 10,
          fillColor: color,
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 2,
        },
      });

      // Info window on click
      const infoWindow = new google.maps.InfoWindow({
        content: `
          <div style="background:#161b22;color:#e6edf3;padding:10px 14px;border-radius:8px;
                      font-family:'DM Sans',sans-serif;min-width:160px;">
            <div style="font-weight:700;color:${color};margin-bottom:4px;">${route.area}</div>
            <div style="font-size:12px;color:#8b949e;">Route: ${route.route_id}</div>
            <div style="font-size:11px;color:#8b949e;margin-top:4px;">
              Stop ${pi + 1} of ${pts.length}<br>
              📍 ${pt.lat.toFixed(5)}, ${pt.lng.toFixed(5)}
            </div>
          </div>`,
      });

      marker.addListener('click', () => infoWindow.open(fullMap, marker));
      allMarkers.push(marker);
    });
  });

  // Build legend
  buildMapLegend(routesData, colors);
}

/** Build route legend below map */
function buildMapLegend(routes, colors) {
  const legendEl = document.getElementById('map-legend');
  if (!legendEl || routes.length === 0) return;
  legendEl.innerHTML = routes.map((r, i) => `
    <div class="legend-item">
      <span class="legend-dot" style="background:${colors[i % colors.length]}"></span>
      <span>${r.route_id} – ${r.area} (${(r.pickup_points||[]).length} stops)</span>
    </div>
  `).join('');
}

/** Filter map to show only one route */
function filterRoute(routeId) {
  // Reload page with filter (simple approach)
  // For a more complex SPA you'd re-render markers
  console.log('Filter route:', routeId);
}


/* ══════════════════════════════════════════════════════════════════════════
   DARK MAP STYLE
   ══════════════════════════════════════════════════════════════════════════ */

function darkMapStyles() {
  return [
    { elementType: 'geometry',       stylers: [{ color: '#212121' }] },
    { elementType: 'labels.text.stroke', stylers: [{ color: '#212121' }] },
    { elementType: 'labels.text.fill',   stylers: [{ color: '#757575' }] },
    { featureType: 'administrative',     elementType: 'geometry', stylers: [{ color: '#757575' }] },
    { featureType: 'road',               elementType: 'geometry', stylers: [{ color: '#2c2c2c' }] },
    { featureType: 'road.highway',       elementType: 'geometry', stylers: [{ color: '#3c3c3c' }] },
    { featureType: 'water',              elementType: 'geometry', stylers: [{ color: '#000000' }] },
    { featureType: 'poi',                elementType: 'geometry', stylers: [{ color: '#1a1a1a' }] },
  ];
}


/* ══════════════════════════════════════════════════════════════════════════
   GENERAL UI UTILITIES
   ══════════════════════════════════════════════════════════════════════════ */

/** Auto-dismiss alerts after 4 seconds */
document.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert.auto-dismiss');
  alerts.forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity    = '0';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  // Highlight active sidebar link
  const path = window.location.pathname;
  document.querySelectorAll('.sidebar nav a').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && path === '/') {
      link.classList.add('active');
    }
  });
});

/** Confirm delete dialog */
function confirmDelete(name) {
  return confirm(`Delete "${name}"? This action cannot be undone.`);
}
