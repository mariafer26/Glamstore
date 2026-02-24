// ============================================================
// GlamStore - JavaScript Principal
// Funcionalidades de interacción para la aplicación web
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // --- Mostrar fecha actual en el header ---
    actualizarFecha();
    
    // --- Sidebar toggle para móviles ---
    configurarMenuMovil();
    
    // --- Auto-cerrar mensajes flash ---
    configurarFlashMessages();
    
});


/**
 * Actualiza la fecha mostrada en el header superior.
 */
function actualizarFecha() {
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        const opciones = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        const fecha = new Date().toLocaleDateString('es-ES', opciones);
        // Capitalizar primera letra
        dateElement.textContent = fecha.charAt(0).toUpperCase() + fecha.slice(1);
    }
}


/**
 * Configura el toggle del menú lateral para dispositivos móviles.
 */
function configurarMenuMovil() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
        
        // Cerrar sidebar al hacer clic fuera de él
        document.addEventListener('click', function(e) {
            if (sidebar.classList.contains('open') && 
                !sidebar.contains(e.target) && 
                !menuToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }
}


/**
 * Configura el auto-cierre de mensajes flash después de 5 segundos.
 */
function configurarFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.3s ease-out';
            
            setTimeout(function() {
                msg.remove();
            }, 300);
        }, 5000);
    });
}
