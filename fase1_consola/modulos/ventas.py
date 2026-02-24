# ============================================================
# Módulo: ventas.py
# Descripción: Registro y control de ventas
# Sistema de Gestión - Tienda de Maquillaje "GlamStore"
# ============================================================
# Funcionalidades:
# - Registrar ventas individuales y múltiples productos
# - Calcular totales de venta
# - Actualizar stock automáticamente
# - Guardar historial de ventas
# ============================================================

from datetime import datetime
from .base_datos import BaseDatos
from .productos import GestionProductos


class GestionVentas:
    """
    Clase para gestionar las ventas de la tienda.
    Registra ventas, calcula totales y actualiza el inventario automáticamente.
    """

    def __init__(self, base_datos, gestion_productos):
        """
        Inicializa el gestor de ventas.
        
        Args:
            base_datos (BaseDatos): Instancia de la base de datos
            gestion_productos (GestionProductos): Instancia del gestor de productos
        """
        self.db = base_datos
        self.productos = gestion_productos

    def registrar_venta(self, items_venta):
        """
        Registra una nueva venta con uno o varios productos.
        
        Cada item de la venta debe tener:
        - id_producto: ID del producto vendido
        - cantidad: Cantidad vendida
        
        El sistema automáticamente:
        - Verifica stock disponible
        - Calcula el total
        - Reduce el stock
        - Guarda el historial
        
        Args:
            items_venta (list): Lista de dicts con {id_producto, cantidad}
            
        Returns:
            dict: Resultado de la operación con detalle de la venta
        """
        if not items_venta:
            return {"exito": False, "mensaje": "La venta debe tener al menos un producto."}
        
        # Verificar disponibilidad de todos los productos antes de procesar
        detalles = []
        total_venta = 0
        alertas = []
        
        for item in items_venta:
            id_producto = item["id_producto"]
            cantidad = item["cantidad"]
            
            # Validar cantidad
            if cantidad <= 0:
                return {"exito": False, "mensaje": f"La cantidad debe ser mayor a 0 para el producto #{id_producto}."}
            
            # Buscar producto
            producto = self.productos.obtener_producto(id_producto)
            if not producto:
                return {"exito": False, "mensaje": f"No se encontró el producto con ID #{id_producto}."}
            
            # Verificar si el producto está activo
            if not producto.get("activo", True):
                return {"exito": False, "mensaje": f"El producto '{producto['nombre']}' no está disponible."}
            
            # Verificar stock
            if cantidad > producto["cantidad_stock"]:
                return {
                    "exito": False,
                    "mensaje": f"Stock insuficiente para '{producto['nombre']}'. "
                              f"Disponible: {producto['cantidad_stock']}, Solicitado: {cantidad}."
                }
            
            # Calcular subtotal
            subtotal = producto["precio"] * cantidad
            total_venta += subtotal
            
            detalles.append({
                "id_producto": id_producto,
                "nombre_producto": producto["nombre"],
                "marca": producto["marca"],
                "precio_unitario": producto["precio"],
                "cantidad": cantidad,
                "subtotal": round(subtotal, 2)
            })
        
        # Procesar la venta: reducir stock de cada producto
        for item in items_venta:
            resultado_stock = self.productos.reducir_stock(item["id_producto"], item["cantidad"])
            if not resultado_stock["exito"]:
                return resultado_stock
            if resultado_stock.get("alerta_stock"):
                alertas.append(resultado_stock["mensaje"])
        
        # Crear registro de venta
        venta = {
            "items": detalles,
            "cantidad_items": len(detalles),
            "total": round(total_venta, 2),
            "metodo_pago": "efectivo"  # Por defecto, expandible en el futuro
        }
        
        # Guardar venta en la base de datos
        id_venta = self.db.guardar_venta(venta)
        
        # Construir mensaje de éxito
        mensaje = f"\n🧾 ¡Venta #{id_venta:03d} registrada exitosamente!"
        mensaje += f"\n{'─' * 50}"
        
        for detalle in detalles:
            mensaje += (
                f"\n  • {detalle['nombre_producto']} ({detalle['marca']})"
                f"\n    {detalle['cantidad']} × ${detalle['precio_unitario']:,.2f} = ${detalle['subtotal']:,.2f}"
            )
        
        mensaje += f"\n{'─' * 50}"
        mensaje += f"\n  💰 TOTAL: ${total_venta:,.2f}"
        mensaje += f"\n{'─' * 50}"
        
        # Agregar alertas de stock si las hay
        if alertas:
            mensaje += "\n\n📢 ALERTAS DE STOCK:"
            for alerta in alertas:
                mensaje += f"\n{alerta}"
        
        return {
            "exito": True,
            "mensaje": mensaje,
            "id_venta": id_venta,
            "total": round(total_venta, 2),
            "detalles": detalles
        }

    def obtener_historial(self, limite=None):
        """
        Obtiene el historial de ventas.
        
        Args:
            limite (int, optional): Número máximo de ventas a retornar.
                                     None para todas.
            
        Returns:
            list: Lista de ventas ordenadas de más reciente a más antigua
        """
        ventas = self.db.obtener_ventas()
        
        # Ordenar por fecha (más reciente primero)
        ventas.sort(key=lambda v: v.get("fecha", ""), reverse=True)
        
        if limite:
            return ventas[:limite]
        
        return ventas

    def obtener_ventas_periodo(self, dias=7):
        """
        Obtiene las ventas de los últimos N días.
        
        Args:
            dias (int): Número de días a consultar (por defecto 7 = una semana)
            
        Returns:
            list: Ventas del período especificado
        """
        ventas = self.db.obtener_ventas()
        ahora = datetime.now()
        
        ventas_periodo = []
        for venta in ventas:
            try:
                fecha_venta = datetime.strptime(venta["fecha"], "%Y-%m-%d %H:%M:%S")
                diferencia = (ahora - fecha_venta).days
                if diferencia <= dias:
                    ventas_periodo.append(venta)
            except (ValueError, KeyError):
                continue
        
        return ventas_periodo

    def calcular_total_periodo(self, dias=7):
        """
        Calcula el total de dinero generado en un período.
        
        Args:
            dias (int): Número de días del período
            
        Returns:
            float: Total de ingresos del período
        """
        ventas = self.obtener_ventas_periodo(dias)
        return sum(v.get("total", 0) for v in ventas)

    @staticmethod
    def formato_venta(venta):
        """
        Formatea una venta para mostrar en consola.
        
        Args:
            venta (dict): Datos de la venta
            
        Returns:
            str: Cadena formateada para mostrar
        """
        texto = f"\n  🧾 Venta #{venta['id']:03d} | Fecha: {venta['fecha']}"
        texto += f"\n  {'─' * 45}"
        
        for item in venta.get("items", []):
            texto += (
                f"\n    • {item['nombre_producto']} × {item['cantidad']}"
                f" = ${item['subtotal']:,.2f}"
            )
        
        texto += f"\n  {'─' * 45}"
        texto += f"\n  💰 Total: ${venta['total']:,.2f}"
        
        return texto
