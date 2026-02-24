# ============================================================
# Rutas del Dashboard (Panel Principal)
# ============================================================

from flask import Blueprint, render_template
from models import obtener_estadisticas_dashboard

# Crear blueprint para el dashboard
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    """
    Página principal del sistema.
    Muestra un resumen general con estadísticas clave.
    """
    stats = obtener_estadisticas_dashboard()
    return render_template('dashboard.html', stats=stats)
