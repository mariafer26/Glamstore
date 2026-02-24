# ============================================================
# Módulo: base_datos.py
# Descripción: Manejo de persistencia de datos usando archivos JSON
# Sistema de Gestión - Tienda de Maquillaje "GlamStore"
# ============================================================
# Este módulo se encarga de:
# - Guardar datos en archivos JSON
# - Cargar datos desde archivos JSON
# - Generar IDs únicos para productos y ventas
# - Crear respaldos automáticos de los datos
# ============================================================

import json
import os
import shutil
from datetime import datetime


class BaseDatos:
    """
    Clase para manejar la persistencia de datos del sistema.
    Guarda y carga información desde archivos JSON.
    """

    def __init__(self, directorio_datos="datos"):
        """
        Inicializa la base de datos con la ruta del directorio de datos.
        
        Args:
            directorio_datos (str): Ruta del directorio donde se guardarán los archivos JSON
        """
        # Obtener la ruta absoluta del directorio de datos
        self.directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.directorio_datos = os.path.join(self.directorio_base, directorio_datos)
        self.directorio_backups = os.path.join(self.directorio_base, "backups")
        
        # Archivos de datos
        self.archivo_productos = os.path.join(self.directorio_datos, "productos.json")
        self.archivo_ventas = os.path.join(self.directorio_datos, "ventas.json")
        self.archivo_config = os.path.join(self.directorio_datos, "config.json")
        
        # Crear directorios si no existen
        self._crear_directorios()
        
        # Inicializar archivos si no existen
        self._inicializar_archivos()

    def _crear_directorios(self):
        """Crea los directorios necesarios para almacenar datos y backups."""
        os.makedirs(self.directorio_datos, exist_ok=True)
        os.makedirs(self.directorio_backups, exist_ok=True)

    def _inicializar_archivos(self):
        """Crea los archivos JSON iniciales si no existen."""
        # Estructura inicial de productos
        if not os.path.exists(self.archivo_productos):
            self._guardar_json(self.archivo_productos, {
                "productos": [],
                "ultimo_id": 0
            })
        
        # Estructura inicial de ventas
        if not os.path.exists(self.archivo_ventas):
            self._guardar_json(self.archivo_ventas, {
                "ventas": [],
                "ultimo_id": 0
            })
        
        # Configuración inicial
        if not os.path.exists(self.archivo_config):
            self._guardar_json(self.archivo_config, {
                "nombre_tienda": "GlamStore",
                "alerta_stock_minimo": 5,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    def _guardar_json(self, archivo, datos):
        """
        Guarda datos en un archivo JSON con formato legible.
        
        Args:
            archivo (str): Ruta del archivo JSON
            datos (dict): Datos a guardar
        """
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"❌ Error al guardar datos: {e}")

    def _cargar_json(self, archivo):
        """
        Carga datos desde un archivo JSON.
        
        Args:
            archivo (str): Ruta del archivo JSON
            
        Returns:
            dict: Datos cargados del archivo, o diccionario vacío si hay error
        """
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"❌ Error al cargar datos: {e}")
            return {}

    # --- Operaciones con Productos ---

    def obtener_productos(self):
        """
        Obtiene la lista completa de productos.
        
        Returns:
            list: Lista de diccionarios con los datos de cada producto
        """
        datos = self._cargar_json(self.archivo_productos)
        return datos.get("productos", [])

    def guardar_producto(self, producto):
        """
        Guarda un nuevo producto y le asigna un ID único.
        
        Args:
            producto (dict): Datos del producto a guardar
            
        Returns:
            int: ID asignado al nuevo producto
        """
        datos = self._cargar_json(self.archivo_productos)
        
        # Generar nuevo ID
        datos["ultimo_id"] += 1
        producto["id"] = datos["ultimo_id"]
        producto["fecha_registro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Agregar producto a la lista
        datos["productos"].append(producto)
        self._guardar_json(self.archivo_productos, datos)
        
        return producto["id"]

    def actualizar_producto(self, id_producto, datos_actualizados):
        """
        Actualiza los datos de un producto existente.
        
        Args:
            id_producto (int): ID del producto a actualizar
            datos_actualizados (dict): Campos a actualizar
            
        Returns:
            bool: True si se actualizó correctamente, False si no se encontró
        """
        datos = self._cargar_json(self.archivo_productos)
        
        for i, producto in enumerate(datos["productos"]):
            if producto["id"] == id_producto:
                # Actualizar solo los campos proporcionados
                for clave, valor in datos_actualizados.items():
                    datos["productos"][i][clave] = valor
                datos["productos"][i]["fecha_actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._guardar_json(self.archivo_productos, datos)
                return True
        
        return False

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto por su ID.
        
        Args:
            id_producto (int): ID del producto a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró
        """
        datos = self._cargar_json(self.archivo_productos)
        productos_antes = len(datos["productos"])
        
        datos["productos"] = [p for p in datos["productos"] if p["id"] != id_producto]
        
        if len(datos["productos"]) < productos_antes:
            self._guardar_json(self.archivo_productos, datos)
            return True
        return False

    def buscar_producto_por_id(self, id_producto):
        """
        Busca un producto por su ID.
        
        Args:
            id_producto (int): ID del producto a buscar
            
        Returns:
            dict or None: Datos del producto o None si no existe
        """
        productos = self.obtener_productos()
        for producto in productos:
            if producto["id"] == id_producto:
                return producto
        return None

    # --- Operaciones con Ventas ---

    def obtener_ventas(self):
        """
        Obtiene la lista completa de ventas.
        
        Returns:
            list: Lista de diccionarios con los datos de cada venta
        """
        datos = self._cargar_json(self.archivo_ventas)
        return datos.get("ventas", [])

    def guardar_venta(self, venta):
        """
        Guarda una nueva venta con ID y fecha automáticos.
        
        Args:
            venta (dict): Datos de la venta
            
        Returns:
            int: ID asignado a la nueva venta
        """
        datos = self._cargar_json(self.archivo_ventas)
        
        # Generar nuevo ID
        datos["ultimo_id"] += 1
        venta["id"] = datos["ultimo_id"]
        venta["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Agregar venta a la lista
        datos["ventas"].append(venta)
        self._guardar_json(self.archivo_ventas, datos)
        
        return venta["id"]

    # --- Operaciones de Configuración ---

    def obtener_config(self):
        """
        Obtiene la configuración del sistema.
        
        Returns:
            dict: Configuración del sistema
        """
        return self._cargar_json(self.archivo_config)

    # --- Backup ---

    def crear_backup(self):
        """
        Crea una copia de seguridad de todos los archivos de datos.
        
        Returns:
            str: Ruta del directorio de backup creado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        directorio_backup = os.path.join(self.directorio_backups, f"backup_{timestamp}")
        
        try:
            shutil.copytree(self.directorio_datos, directorio_backup)
            return directorio_backup
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
            return None
