# ============================================================
# Rutas del Módulo de Reportes
# ============================================================

from flask import Blueprint, render_template
from models import generar_reporte_semanal

# Crear blueprint para reportes
reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')


@reportes_bp.route('/semanal')
def semanal():
    """Muestra el reporte semanal."""
    reporte = generar_reporte_semanal()
    return render_template('reportes/semanal.html', reporte=reporte)
