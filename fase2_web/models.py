# ============================================================
# Modelos de Base de Datos (SQLite)
# Sistema de Gestión - Tienda de Maquillaje "GlamStore"
# ============================================================
# Modelos definidos:
# - Producto: Inventario de productos de maquillaje
# - Venta: Registro de ventas realizadas
# - DetalleVenta: Items individuales de cada venta
# ============================================================

import sqlite3
import os
from datetime import datetime, timedelta
from collections import Counter


# Ruta de la base de datos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "glamstore.db")


def get_db():
    """
    Obtiene una conexión a la base de datos SQLite.
    
    Returns:
        sqlite3.Connection: Conexión a la base de datos
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retorna filas como diccionarios
    conn.execute("PRAGMA foreign_keys = ON")  # Habilitar claves foráneas
    return conn


def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias.
    Se ejecuta al iniciar la aplicación por primera vez.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL CHECK(precio > 0),
            cantidad_stock INTEGER NOT NULL DEFAULT 0 CHECK(cantidad_stock >= 0),
            activo INTEGER NOT NULL DEFAULT 1,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL DEFAULT 0,
            cantidad_items INTEGER NOT NULL DEFAULT 0,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de detalles de venta (items individuales)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalles_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            nombre_producto TEXT NOT NULL,
            marca_producto TEXT NOT NULL,
            precio_unitario REAL NOT NULL,
            cantidad INTEGER NOT NULL CHECK(cantidad > 0),
            subtotal REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')
    
    conn.commit()
    conn.close()


# ============================================================
# FUNCIONES DE PRODUCTOS
# ============================================================

def obtener_productos(solo_activos=True, categoria=None, stock_bajo=False, stock_minimo=5):
    """
    Obtiene la lista de productos con filtros opcionales.
    
    Args:
        solo_activos (bool): Solo productos activos
        categoria (str): Filtrar por categoría
        stock_bajo (bool): Solo productos con stock bajo
        stock_minimo (int): Umbral de stock bajo
        
    Returns:
        list: Lista de productos como diccionarios
    """
    conn = get_db()
    query = "SELECT * FROM productos WHERE 1=1"
    params = []
    
    if solo_activos:
        query += " AND activo = 1"
    
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    
    if stock_bajo:
        query += " AND cantidad_stock <= ? AND activo = 1"
        params.append(stock_minimo)
    
    query += " ORDER BY nombre ASC"
    
    productos = conn.execute(query, params).fetchall()
    conn.close()
    
    return [dict(p) for p in productos]


def obtener_producto_por_id(producto_id):
    """
    Obtiene un producto por su ID.
    
    Args:
        producto_id (int): ID del producto
        
    Returns:
        dict or None: Datos del producto o None
    """
    conn = get_db()
    producto = conn.execute("SELECT * FROM productos WHERE id = ?", (producto_id,)).fetchone()
    conn.close()
    
    return dict(producto) if producto else None


def crear_producto(nombre, marca, categoria, precio, cantidad_stock):
    """
    Crea un nuevo producto en la base de datos.
    
    Args:
        nombre (str): Nombre del producto
        marca (str): Marca del producto
        categoria (str): Categoría
        precio (float): Precio de venta
        cantidad_stock (int): Stock inicial
        
    Returns:
        int: ID del nuevo producto
    """
    conn = get_db()
    cursor = conn.execute(
        '''INSERT INTO productos (nombre, marca, categoria, precio, cantidad_stock)
           VALUES (?, ?, ?, ?, ?)''',
        (nombre.strip().title(), marca.strip().title(), categoria, round(precio, 2), cantidad_stock)
    )
    conn.commit()
    producto_id = cursor.lastrowid
    conn.close()
    
    return producto_id


def actualizar_producto(producto_id, datos):
    """
    Actualiza un producto existente.
    
    Args:
        producto_id (int): ID del producto
        datos (dict): Campos a actualizar
        
    Returns:
        bool: True si se actualizó correctamente
    """
    conn = get_db()
    
    campos = []
    valores = []
    
    for campo, valor in datos.items():
        if campo in ['nombre', 'marca', 'categoria', 'precio', 'cantidad_stock']:
            campos.append(f"{campo} = ?")
            valores.append(valor)
    
    if not campos:
        conn.close()
        return False
    
    campos.append("fecha_actualizacion = CURRENT_TIMESTAMP")
    valores.append(producto_id)
    
    query = f"UPDATE productos SET {', '.join(campos)} WHERE id = ?"
    conn.execute(query, valores)
    conn.commit()
    conn.close()
    
    return True


def eliminar_producto(producto_id):
    """
    Elimina (desactiva) un producto.
    
    Args:
        producto_id (int): ID del producto
        
    Returns:
        bool: True si se eliminó correctamente
    """
    conn = get_db()
    conn.execute(
        "UPDATE productos SET activo = 0, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
        (producto_id,)
    )
    conn.commit()
    conn.close()
    return True


def reducir_stock(producto_id, cantidad):
    """
    Reduce el stock de un producto.
    
    Args:
        producto_id (int): ID del producto
        cantidad (int): Cantidad a reducir
        
    Returns:
        dict: Resultado con éxito, mensaje y alerta de stock
    """
    producto = obtener_producto_por_id(producto_id)
    
    if not producto:
        return {"exito": False, "mensaje": "Producto no encontrado."}
    
    if cantidad > producto["cantidad_stock"]:
        return {"exito": False, "mensaje": f"Stock insuficiente. Disponible: {producto['cantidad_stock']}"}
    
    nuevo_stock = producto["cantidad_stock"] - cantidad
    actualizar_producto(producto_id, {"cantidad_stock": nuevo_stock})
    
    resultado = {"exito": True, "nuevo_stock": nuevo_stock}
    
    if nuevo_stock <= 5:
        resultado["alerta_stock"] = True
    
    return resultado


# ============================================================
# FUNCIONES DE VENTAS
# ============================================================

def registrar_venta(items):
    """
    Registra una nueva venta con sus detalles.
    
    Args:
        items (list): Lista de dicts con {producto_id, cantidad}
        
    Returns:
        dict: Resultado de la operación
    """
    conn = get_db()
    
    try:
        total_venta = 0
        detalles = []
        
        # Validar todos los items primero
        for item in items:
            producto = obtener_producto_por_id(item["producto_id"])
            
            if not producto:
                return {"exito": False, "mensaje": f"Producto #{item['producto_id']} no encontrado."}
            
            if not producto.get("activo", 1):
                return {"exito": False, "mensaje": f"'{producto['nombre']}' no está disponible."}
            
            if item["cantidad"] > producto["cantidad_stock"]:
                return {
                    "exito": False,
                    "mensaje": f"Stock insuficiente para '{producto['nombre']}'. Disponible: {producto['cantidad_stock']}"
                }
            
            subtotal = producto["precio"] * item["cantidad"]
            total_venta += subtotal
            
            detalles.append({
                "producto_id": producto["id"],
                "nombre_producto": producto["nombre"],
                "marca_producto": producto["marca"],
                "precio_unitario": producto["precio"],
                "cantidad": item["cantidad"],
                "subtotal": round(subtotal, 2)
            })
        
        # Crear registro de venta
        cursor = conn.execute(
            "INSERT INTO ventas (total, cantidad_items) VALUES (?, ?)",
            (round(total_venta, 2), len(detalles))
        )
        venta_id = cursor.lastrowid
        
        # Guardar detalles y actualizar stock
        alertas = []
        for detalle in detalles:
            conn.execute(
                '''INSERT INTO detalles_venta 
                   (venta_id, producto_id, nombre_producto, marca_producto, precio_unitario, cantidad, subtotal)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (venta_id, detalle["producto_id"], detalle["nombre_producto"],
                 detalle["marca_producto"], detalle["precio_unitario"],
                 detalle["cantidad"], detalle["subtotal"])
            )
            
            # Reducir stock
            conn.execute(
                "UPDATE productos SET cantidad_stock = cantidad_stock - ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
                (detalle["cantidad"], detalle["producto_id"])
            )
            
            # Verificar stock bajo
            producto_actualizado = conn.execute(
                "SELECT cantidad_stock, nombre FROM productos WHERE id = ?",
                (detalle["producto_id"],)
            ).fetchone()
            
            if producto_actualizado and producto_actualizado["cantidad_stock"] <= 5:
                alertas.append({
                    "nombre": producto_actualizado["nombre"],
                    "stock": producto_actualizado["cantidad_stock"]
                })
        
        conn.commit()
        conn.close()
        
        return {
            "exito": True,
            "venta_id": venta_id,
            "total": round(total_venta, 2),
            "detalles": detalles,
            "alertas": alertas
        }
    
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"exito": False, "mensaje": f"Error al registrar venta: {str(e)}"}


def obtener_ventas(limite=None):
    """
    Obtiene el historial de ventas.
    
    Args:
        limite (int, optional): Número máximo de ventas
        
    Returns:
        list: Lista de ventas con sus detalles
    """
    conn = get_db()
    
    query = "SELECT * FROM ventas ORDER BY fecha DESC"
    if limite:
        query += f" LIMIT {limite}"
    
    ventas = conn.execute(query).fetchall()
    
    resultado = []
    for venta in ventas:
        venta_dict = dict(venta)
        
        # Obtener detalles de la venta
        detalles = conn.execute(
            "SELECT * FROM detalles_venta WHERE venta_id = ?",
            (venta["id"],)
        ).fetchall()
        
        venta_dict["detalles"] = [dict(d) for d in detalles]
        resultado.append(venta_dict)
    
    conn.close()
    return resultado


def obtener_venta_por_id(venta_id):
    """Obtiene una venta específica por su ID."""
    conn = get_db()
    
    venta = conn.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,)).fetchone()
    
    if not venta:
        conn.close()
        return None
    
    venta_dict = dict(venta)
    
    detalles = conn.execute(
        "SELECT * FROM detalles_venta WHERE venta_id = ?",
        (venta_id,)
    ).fetchall()
    
    venta_dict["detalles"] = [dict(d) for d in detalles]
    
    conn.close()
    return venta_dict


def obtener_ventas_periodo(dias=7):
    """
    Obtiene las ventas de los últimos N días.
    
    Args:
        dias (int): Número de días
        
    Returns:
        list: Ventas del período
    """
    conn = get_db()
    
    fecha_inicio = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d %H:%M:%S")
    
    ventas = conn.execute(
        "SELECT * FROM ventas WHERE fecha >= ? ORDER BY fecha DESC",
        (fecha_inicio,)
    ).fetchall()
    
    resultado = []
    for venta in ventas:
        venta_dict = dict(venta)
        detalles = conn.execute(
            "SELECT * FROM detalles_venta WHERE venta_id = ?",
            (venta["id"],)
        ).fetchall()
        venta_dict["detalles"] = [dict(d) for d in detalles]
        resultado.append(venta_dict)
    
    conn.close()
    return resultado


# ============================================================
# FUNCIONES DE REPORTES
# ============================================================

def generar_reporte_semanal():
    """
    Genera un reporte completo de la última semana.
    
    Returns:
        dict: Reporte con todas las métricas
    """
    ventas_semana = obtener_ventas_periodo(dias=7)
    
    total_ventas = len(ventas_semana)
    total_ingresos = sum(v.get("total", 0) for v in ventas_semana)
    promedio_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
    
    # Productos más vendidos
    contador_productos = Counter()
    ingresos_por_producto = Counter()
    ventas_por_categoria = Counter()
    
    for venta in ventas_semana:
        for item in venta.get("detalles", []):
            nombre = item.get("nombre_producto", "Desconocido")
            cantidad = item.get("cantidad", 0)
            subtotal = item.get("subtotal", 0)
            
            contador_productos[nombre] += cantidad
            ingresos_por_producto[nombre] += subtotal
            
            producto = obtener_producto_por_id(item.get("producto_id"))
            if producto:
                ventas_por_categoria[producto.get("categoria", "Sin categoría")] += cantidad
    
    productos_mas_vendidos = contador_productos.most_common(5)
    
    # Productos con stock bajo
    stock_bajo = obtener_productos(stock_bajo=True)
    
    return {
        "periodo": {
            "inicio": (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y"),
            "fin": datetime.now().strftime("%d/%m/%Y")
        },
        "total_ventas": total_ventas,
        "total_ingresos": round(total_ingresos, 2),
        "promedio_por_venta": round(promedio_venta, 2),
        "productos_mas_vendidos": [
            {"nombre": nombre, "cantidad": cant}
            for nombre, cant in productos_mas_vendidos
        ],
        "ingresos_por_producto": [
            {"nombre": nombre, "ingresos": round(ingreso, 2)}
            for nombre, ingreso in ingresos_por_producto.most_common(5)
        ],
        "ventas_por_categoria": [
            {"categoria": cat, "cantidad": cant}
            for cat, cant in ventas_por_categoria.most_common()
        ],
        "productos_stock_bajo": len(stock_bajo),
        "alertas_stock": [
            {"id": p["id"], "nombre": p["nombre"], "stock": p["cantidad_stock"]}
            for p in stock_bajo
        ]
    }


def obtener_estadisticas_dashboard():
    """
    Obtiene las estadísticas para el panel principal.
    
    Returns:
        dict: Estadísticas del dashboard
    """
    productos = obtener_productos()
    stock_bajo = obtener_productos(stock_bajo=True)
    ventas_semana = obtener_ventas_periodo(dias=7)
    todas_ventas = obtener_ventas()
    
    total_ingresos_semana = sum(v.get("total", 0) for v in ventas_semana)
    total_ingresos_total = sum(v.get("total", 0) for v in todas_ventas)
    
    total_unidades = sum(p["cantidad_stock"] for p in productos)
    valor_inventario = sum(p["precio"] * p["cantidad_stock"] for p in productos)
    
    # Ventas de hoy
    hoy = datetime.now().strftime("%Y-%m-%d")
    ventas_hoy = [v for v in ventas_semana if v.get("fecha", "").startswith(hoy)]
    ingresos_hoy = sum(v.get("total", 0) for v in ventas_hoy)
    
    return {
        "total_productos": len(productos),
        "total_unidades": total_unidades,
        "productos_stock_bajo": len(stock_bajo),
        "alertas_stock": stock_bajo[:5],  # Top 5 alertas
        "ventas_semana": len(ventas_semana),
        "ingresos_semana": round(total_ingresos_semana, 2),
        "ventas_hoy": len(ventas_hoy),
        "ingresos_hoy": round(ingresos_hoy, 2),
        "total_ventas_historico": len(todas_ventas),
        "ingresos_totales": round(total_ingresos_total, 2),
        "valor_inventario": round(valor_inventario, 2),
        "ventas_recientes": ventas_semana[:5]  # Últimas 5 ventas
    }
