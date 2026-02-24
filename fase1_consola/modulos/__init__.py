# ============================================================
# Módulo de inicialización del paquete 'modulos'
# Sistema de Gestión - Tienda de Maquillaje "GlamStore"
# ============================================================
# Este paquete contiene los módulos principales del sistema:
# - productos: Gestión de productos (CRUD)
# - ventas: Registro y control de ventas
# - reportes: Generación de reportes semanales
# - base_datos: Persistencia de datos en JSON
# ============================================================

from .base_datos import BaseDatos
from .productos import GestionProductos
from .ventas import GestionVentas
from .reportes import GeneradorReportes

__all__ = ['BaseDatos', 'GestionProductos', 'GestionVentas', 'GeneradorReportes']
