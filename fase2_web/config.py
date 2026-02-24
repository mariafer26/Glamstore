# ============================================================
# Configuración de la aplicación Flask
# Sistema de Gestión - Tienda de Maquillaje "GlamStore"
# ============================================================

import os


class Config:
    """Configuración base de la aplicación."""
    
    # Clave secreta para sesiones y CSRF (cambiar en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'glamstore-clave-secreta-dev-2024'
    
    # Ruta de la base de datos SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "glamstore.db")}'
    
    # Deshabilitar señales de modificación (mejora rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Nombre de la tienda
    NOMBRE_TIENDA = "GlamStore"
    
    # Umbral de stock bajo
    STOCK_MINIMO = 5
    
    # Categorías de productos disponibles
    CATEGORIAS = [
        "Labiales",
        "Shampoo",
        "Acondicionador",
        "Tónicos",
        "Tratamientos",
        "Mascarillas",
        "Termo-protectores",
        "Bombonera",
        "Serums",
        "Bases",
        "Sombras",
        "Rubores",
        "Correctores",
        "Máscaras de pestañas",
        "Delineadores",
        "Polvos",
        "Primers",
        "Brochas y herramientas",
        "Skincare",
        "Perfumes",
        "Uñas",
        "Accesorios",
        "Ampollas",
        "Otro"
    ]

    # Marcas disponibles
    MARCAS = [
        "Atenea",
        "Poción",
        "Menta Hair",
        "Mac",
        "Maybelline",
        "Milagros",
        "Bloomshell",
        "Kaba",
        "Anyeluz",
        "Origen Botánico",
        "Rubee",
        "Ruby Rose",
        "Lula",
        "Ani-K",
        "Prosa",
        "Otro"
    ]


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    # En producción, usar variable de entorno para la clave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY')


# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
