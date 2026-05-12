// Cambiar navbar al hacer scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled', 'bg-black');
        navbar.classList.remove('bg-dark');
    } else {
        navbar.classList.remove('navbar-scrolled', 'bg-black');
        navbar.classList.add('bg-dark');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const offcanvasEl = document.getElementById('notificationOffcanvas');
    if (offcanvasEl) {
        // Cargar notificaciones cuando se abre el offcanvas
        offcanvasEl.addEventListener('show.bs.offcanvas', function () {
            // Mostrar un estado de carga muy breve
            const container = document.getElementById('notificationList');
            container.innerHTML = '<div class="notification-empty"><i class="bi bi-hourglass-split"></i> Cargando...</div>';
            // Pequeño delay para asegurar que el offcanvas está visible
            setTimeout(() => loadNotifications(), 100);
        });
    }
    
    // Actualizar badge cada 30 segundos
    setInterval(updateBadge, 30000);
    // Actualizar notificaciones cada 30 segundos si el offcanvas está abierto
    setInterval(function() {
        if (document.getElementById('notificationOffcanvas').classList.contains('show')) {
            loadNotifications();
        }
    }, 30000);
});

function loadNotifications() {
    const container = document.getElementById('notificationList');
    fetch('/api/notifications/')
        .then(r => r.json())
        .then(data => {
            const notifs = data.notifications || [];
            if (notifs.length === 0) {
                container.innerHTML = '<div class="notification-empty"><i class="bi bi-inbox"></i> <p>No hay notificaciones</p></div>';
                return;
            }
            container.innerHTML = notifs.map(n => `
                <div class="notification-item ${n.is_read ? 'opacity-50' : ''}">
                    <strong>${escapeHtml(n.title)}</strong>
                    <div class="notification-message">${escapeHtml(n.message)}</div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="notification-date">${formatDate(n.created_at)}</small>
                        ${!n.is_read ? `<button class="btn btn-sm" onclick="markNotification(${n.id})">Marcar leído</button>` : '<span style="color:#666; font-size:0.8rem;">Leído</span>'}
                    </div>
                </div>
            `).join('');
        })
        .catch(err => { 
            container.innerHTML = '<div class="notification-empty"><i class="bi bi-exclamation-circle"></i> <p>Error cargando notificaciones</p></div>';
            console.error(err); 
        });
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Hace unos segundos';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours}h`;
    if (diffDays < 7) return `Hace ${diffDays} días`;
    return date.toLocaleDateString('es-ES');
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function markNotification(id) {
    fetch(`/api/notifications/${id}/mark-read/`, {method: 'POST', headers: {'X-CSRFToken': getCSRF(), 'Content-Type':'application/json'}})
        .then(r => r.json())
        .then(() => { loadNotifications(); updateBadge(); })
        .catch(e => console.error(e));
}

function updateBadge() {
    fetch('/api/notifications/unread-count/')
        .then(r => r.json())
        .then(data => {
            const count = data.unread_count || 0;
            const bell = document.getElementById('notificationBell');
            if (!bell) return;
            let badge = bell.querySelector('.badge');
            if (count > 0) {
                if (!badge) {
                    badge = document.createElement('span');
                    badge.className = 'position-absolute top-50 start-100 translate-middle badge rounded-pill bg-danger';
                    badge.style.fontSize = '11px';
                    badge.style.padding = '4px 6px';
                    bell.appendChild(badge);
                }
                badge.textContent = count;
            } else if (badge) {
                badge.remove();
            }
        })
        .catch(err => console.error(err));
}

function getCSRF() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}
