/**
 * WasteTrack Smart City — Base JavaScript
 * Loaded on every page via base.html
 */

// ── Bootstrap Tooltip Init ────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Init all Bootstrap tooltips
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(el => new bootstrap.Tooltip(el));

  // Animate stat values on page load (count-up effect)
  animateCounters();

  // Auto-dismiss alerts after 5 seconds
  autoDismissAlerts();

  // Add active class to collapse headers when open
  setupCollapseIcons();
});

// ── Counter Animation ─────────────────────────────────────────────────────
function animateCounters() {
  const counters = document.querySelectorAll('.stat-value');
  counters.forEach(counter => {
    const target = parseInt(counter.textContent, 10);
    if (isNaN(target) || target === 0) return;
    let current = 0;
    const step = Math.ceil(target / 30);
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      counter.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 20);
  });
}

// ── Auto-dismiss Alerts ───────────────────────────────────────────────────
function autoDismissAlerts() {
  const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });
}

// ── Collapse Icon Toggle ──────────────────────────────────────────────────
function setupCollapseIcons() {
  document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(toggle => {
    const icon = toggle.querySelector('.bi-chevron-down');
    if (!icon) return;
    const target = document.querySelector(toggle.getAttribute('data-bs-target'));
    if (!target) return;
    target.addEventListener('show.bs.collapse', () => {
      icon.style.transform = 'rotate(180deg)';
      icon.style.transition = 'transform 0.3s ease';
    });
    target.addEventListener('hide.bs.collapse', () => {
      icon.style.transform = 'rotate(0deg)';
    });
  });
}

// ── Table Row Highlight ───────────────────────────────────────────────────
document.querySelectorAll('table tbody tr').forEach(row => {
  row.style.cursor = 'default';
});
