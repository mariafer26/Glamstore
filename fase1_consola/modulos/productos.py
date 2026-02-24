# ============================================================
# Módulo: productos.py
# Descripción: Gestión completa de productos (CRUD)
# Sistema de Gestión - Tienda de Maquillaje "GlamStore"
# ============================================================
# Funcionalidades:
# - Registrar nuevos productos
# - Listar productos (todos o filtrados)
# - Actualizar stock y datos de productos
# - Eliminar productos
# - Alertas de stock bajo
# ============================================================

from .base_datos import BaseDatos


# Categorías válidas para productos de maquillaje
CATEGORIAS_VALIDAS = [
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
    "Brochas",
    "Skincare",
    "Perfumes",
    "Uñas",
    "Accesorios",
    "Ampollas",
    "Otro"
]

# Marcas válidas
MARCAS_VALIDAS = [
    "Atenea",
    "Poción",
    "Menta Hair",
    "Mac",
    "Maybelline",
    "Urban Decay",
    "Clinique",
    "Nars",
    "Vogue",
    "Otro"
]


class GestionProductos:
    """
    Clase para gestionar el inventario de productos de maquillaje.
    Permite registrar, listar, actualizar y eliminar productos.
    """

    def __init__(self, base_datos):
        """
        Inicializa el gestor de productos.
        
        Args:
            base_datos (BaseDatos): Instancia de la base de datos
        """
        self.db = base_datos
        self.stock_minimo = 5  # Umbral para alerta de stock bajo

    def registrar_producto(self, nombre, marca, categoria, precio, cantidad):
        """
        Registra un nuevo producto en el inventario.
        
        Args:
            nombre (str): Nombre del producto
            marca (str): Marca del producto
            categoria (str): Categoría del producto
            precio (float): Precio de venta
            cantidad (int): Cantidad inicial en stock
            
        Returns:
            dict: Resultado de la operación con éxito/error y mensaje
        """
        # Validaciones
        if not nombre or not nombre.strip():
            return {"exito": False, "mensaje": "El nombre del producto es obligatorio."}
        
        if marca not in MARCAS_VALIDAS:
            return {"exito": False, "mensaje": f"Marca no válida. Opciones: {', '.join(MARCAS_VALIDAS)}"}
        
        if categoria not in CATEGORIAS_VALIDAS:
            return {"exito": False, "mensaje": f"Categoría no válida. Opciones: {', '.join(CATEGORIAS_VALIDAS)}"}
        
        if precio <= 0:
            return {"exito": False, "mensaje": "El precio debe ser mayor a 0."}
        
        if cantidad < 0:
            return {"exito": False, "mensaje": "La cantidad no puede ser negativa."}
        
        # Crear diccionario del producto
        producto = {
            "nombre": nombre.strip().title(),
            "marca": marca,
            "categoria": categoria,
            "precio": round(precio, 2),
            "cantidad_stock": cantidad,
            "activo": True
        }
        
        # Guardar en la base de datos
        id_producto = self.db.guardar_producto(producto)
        
        mensaje = f"✅ Producto '{nombre}' registrado exitosamente con ID #{id_producto}."
        
        # Verificar si el stock inicial es bajo
        if cantidad <= self.stock_minimo:
            mensaje += f"\n⚠️  ¡Atención! El stock inicial es bajo ({cantidad} unidades)."
        
        return {"exito": True, "mensaje": mensaje, "id": id_producto}

    def listar_productos(self, filtro_categoria=None, solo_stock_bajo=False):
        """
        Lista los productos del inventario con opciones de filtrado.
        
        Args:
            filtro_categoria (str, optional): Filtrar por categoría
            solo_stock_bajo (bool): Mostrar solo productos con stock bajo
            
        Returns:
            list: Lista de productos que cumplen los criterios
        """
        productos = self.db.obtener_productos()
        
        # Filtrar solo productos activos
        productos = [p for p in productos if p.get("activo", True)]
        
        # Aplicar filtro de categoría si se especifica
        if filtro_categoria:
            productos = [p for p in productos if p["categoria"] == filtro_categoria]
        
        # Filtrar por stock bajo si se solicita
        if solo_stock_bajo:
            productos = [p for p in productos if p["cantidad_stock"] <= self.stock_minimo]
        
        return productos

    def obtener_producto(self, id_producto):
        """
        Obtiene un producto por su ID.
        
        Args:
            id_producto (int): ID del producto
            
        Returns:
            dict or None: Datos del producto o None si no existe
        """
        return self.db.buscar_producto_por_id(id_producto)

    def actualizar_stock(self, id_producto, nueva_cantidad):
        """
        Actualiza la cantidad en stock de un producto.
        
        Args:
            id_producto (int): ID del producto
            nueva_cantidad (int): Nueva cantidad en stock
            
        Returns:
            dict: Resultado de la operación
        """
        if nueva_cantidad < 0:
            return {"exito": False, "mensaje": "La cantidad no puede ser negativa."}
        
        producto = self.db.buscar_producto_por_id(id_producto)
        if not producto:
            return {"exito": False, "mensaje": f"No se encontró el producto con ID #{id_producto}."}
        
        exito = self.db.actualizar_producto(id_producto, {"cantidad_stock": nueva_cantidad})
        
        if exito:
            mensaje = f"✅ Stock de '{producto['nombre']}' actualizado a {nueva_cantidad} unidades."
            if nueva_cantidad <= self.stock_minimo:
                mensaje += f"\n⚠️  ¡Alerta! Stock bajo ({nueva_cantidad} unidades)."
            return {"exito": True, "mensaje": mensaje}
        
        return {"exito": False, "mensaje": "Error al actualizar el stock."}

    def actualizar_producto(self, id_producto, datos):
        """
        Actualiza los datos generales de un producto.
        
        Args:
            id_producto (int): ID del producto
            datos (dict): Datos a actualizar (nombre, marca, precio, etc.)
            
        Returns:
            dict: Resultado de la operación
        """
        producto = self.db.buscar_producto_por_id(id_producto)
        if not producto:
            return {"exito": False, "mensaje": f"No se encontró el producto con ID #{id_producto}."}
        
        # Validar datos si se proporcionan
        if "precio" in datos and datos["precio"] <= 0:
            return {"exito": False, "mensaje": "El precio debe ser mayor a 0."}
        
        if "marca" in datos and datos["marca"] not in MARCAS_VALIDAS:
            return {"exito": False, "mensaje": "Marca no válida."}
            
        if "categoria" in datos and datos["categoria"] not in CATEGORIAS_VALIDAS:
            return {"exito": False, "mensaje": "Categoría no válida."}
        
        exito = self.db.actualizar_producto(id_producto, datos)
        
        if exito:
            return {"exito": True, "mensaje": f"✅ Producto '{producto['nombre']}' actualizado correctamente."}
        
        return {"exito": False, "mensaje": "Error al actualizar el producto."}

    def eliminar_producto(self, id_producto):
        """
        Elimina (desactiva) un producto del inventario.
        
        Args:
            id_producto (int): ID del producto a eliminar
            
        Returns:
            dict: Resultado de la operación
        """
        producto = self.db.buscar_producto_por_id(id_producto)
        if not producto:
            return {"exito": False, "mensaje": f"No se encontró el producto con ID #{id_producto}."}
        
        # Eliminación lógica (marcar como inactivo) para mantener historial
        exito = self.db.actualizar_producto(id_producto, {"activo": False})
        
        if exito:
            return {"exito": True, "mensaje": f"✅ Producto '{producto['nombre']}' eliminado del inventario."}
        
        return {"exito": False, "mensaje": "Error al eliminar el producto."}

    def reducir_stock(self, id_producto, cantidad):
        """
        Reduce el stock de un producto (usado al registrar ventas).
        
        Args:
            id_producto (int): ID del producto
            cantidad (int): Cantidad a reducir
            
        Returns:
            dict: Resultado de la operación
        """
        producto = self.db.buscar_producto_por_id(id_producto)
        if not producto:
            return {"exito": False, "mensaje": "Producto no encontrado."}
        
        stock_actual = producto["cantidad_stock"]
        
        if cantidad > stock_actual:
            return {
                "exito": False, 
                "mensaje": f"Stock insuficiente. Disponible: {stock_actual} unidades."
            }
        
        nuevo_stock = stock_actual - cantidad
        self.db.actualizar_producto(id_producto, {"cantidad_stock": nuevo_stock})
        
        resultado = {
            "exito": True,
            "mensaje": f"Stock actualizado. Restante: {nuevo_stock} unidades."
        }
        
        # Alerta de stock bajo
        if nuevo_stock <= self.stock_minimo:
            resultado["alerta_stock"] = True
            resultado["mensaje"] += f"\n⚠️  ¡ALERTA! '{producto['nombre']}' tiene stock bajo ({nuevo_stock} unidades). ¡Reabastecer pronto!"
        
        return resultado

    def obtener_alertas_stock(self):
        """
        Obtiene la lista de productos con stock bajo (≤ 5 unidades).
        
        Returns:
            list: Productos con stock bajo
        """
        return self.listar_productos(solo_stock_bajo=True)

    def buscar_productos(self, termino):
        """
        Busca productos por nombre o marca.
        
        Args:
            termino (str): Término de búsqueda
            
        Returns:
            list: Productos que coinciden con la búsqueda
        """
        productos = self.db.obtener_productos()
        termino = termino.lower().strip()
        
        return [
            p for p in productos 
            if p.get("activo", True) and (
                termino in p["nombre"].lower() or 
                termino in p["marca"].lower()
            )
        ]

    @staticmethod
    def mostrar_categorias():
        """Muestra las categorías disponibles con su número."""
        print("\n📋 Categorías disponibles:")
        print("─" * 35)
        for i, cat in enumerate(CATEGORIAS_VALIDAS, 1):
            print(f"  {i:2d}. {cat}")
        print("─" * 35)

    @staticmethod
    def mostrar_marcas():
        """Muestra las marcas disponibles con su número."""
        print("\n🏷️  Marcas disponibles:")
        print("─" * 35)
        for i, marca in enumerate(MARCAS_VALIDAS, 1):
            print(f"  {i:2d}. {marca}")
        print("─" * 35)

    @staticmethod
    def formato_tabla_producto(producto):
        """
        Formatea los datos de un producto para mostrar en consola.
        
        Args:
            producto (dict): Datos del producto
            
        Returns:
            str: Cadena formateada para mostrar
        """
        stock = producto['cantidad_stock']
        indicador_stock = "🟢" if stock > 5 else ("🟡" if stock > 0 else "🔴")
        
        return (
            f"  {indicador_stock} ID: #{producto['id']:03d} | "
            f"{producto['nombre']:<25} | "
            f"Marca: {producto['marca']:<15} | "
            f"Cat: {producto['categoria']:<20} | "
            f"${producto['precio']:>10,.2f} | "
            f"Stock: {stock:>4d} uds"
        )
