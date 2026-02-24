#!/usr/bin/env python3
# ============================================================
# GlamStore - Sistema de Gestión para Tienda de Maquillaje
# Versión: 2.0 (Web con Flask)
# ============================================================
# Instrucciones de ejecución:
#   1. pip install -r requirements.txt
#   2. python app.py
#   3. Abrir navegador en http://localhost:5000
# ============================================================

from flask import Flask
from config import Config
from models import init_db
from routes.dashboard import dashboard_bp
from routes.productos import productos_bp
from routes.ventas import ventas_bp
from routes.reportes import reportes_bp


def create_app():
    """
    Factory function para crear la aplicación Flask.
    Permite crear múltiples instancias y facilita testing.
    
    Returns:
        Flask: Instancia de la aplicación configurada
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar base de datos
    with app.app_context():
        init_db()
    
    # Registrar blueprints (módulos de rutas)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(reportes_bp)
    
    # Filtro personalizado para formato de moneda
    @app.template_filter('moneda')
    def formato_moneda(valor):
        """Formatea un valor numérico como moneda."""
        try:
            return f"${valor:,.2f}"
        except (ValueError, TypeError):
            return "$0.00"
    
    # Manejadores de errores
    @app.errorhandler(404)
    def pagina_no_encontrada(e):
        return "<h1>404 - Página no encontrada</h1><p><a href='/'>Volver al inicio</a></p>", 404
    
    @app.errorhandler(500)
    def error_interno(e):
        return "<h1>500 - Error interno del servidor</h1><p><a href='/'>Volver al inicio</a></p>", 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("\n💄 GlamStore - Sistema de Gestión")
    print("=" * 40)
    print("🌐 Servidor iniciado en: http://localhost:5001")
    print("🛑 Presiona Ctrl+C para detener\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
