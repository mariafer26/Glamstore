# ============================================================
# Módulo: reportes.py
# Descripción: Generación de reportes semanales y estadísticas
# Sistema de Gestión - Tienda de Maquillaje "GlamStore"
# ============================================================
# Funcionalidades:
# - Reporte semanal con ventas totales e ingresos
# - Productos más vendidos
# - Análisis de categorías más populares
# - Estadísticas generales del inventario
# ============================================================

from datetime import datetime, timedelta
from collections import Counter
from .base_datos import BaseDatos
from .ventas import GestionVentas
from .productos import GestionProductos


class GeneradorReportes:
    """
    Clase para generar reportes y estadísticas del negocio.
    Analiza ventas, ingresos y tendencias de productos.
    """

    def __init__(self, base_datos, gestion_productos, gestion_ventas):
        """
        Inicializa el generador de reportes.
        
        Args:
            base_datos (BaseDatos): Instancia de la base de datos
            gestion_productos (GestionProductos): Instancia del gestor de productos
            gestion_ventas (GestionVentas): Instancia del gestor de ventas
        """
        self.db = base_datos
        self.productos = gestion_productos
        self.ventas = gestion_ventas

    def reporte_semanal(self):
        """
        Genera un reporte completo de la última semana.
        
        Returns:
            dict: Reporte con ventas, ingresos, productos más vendidos, etc.
        """
        # Obtener ventas de la última semana
        ventas_semana = self.ventas.obtener_ventas_periodo(dias=7)
        
        # Calcular métricas principales
        total_ventas = len(ventas_semana)
        total_ingresos = sum(v.get("total", 0) for v in ventas_semana)
        
        # Calcular productos más vendidos
        contador_productos = Counter()
        ingresos_por_producto = Counter()
        
        for venta in ventas_semana:
            for item in venta.get("items", []):
                nombre = item.get("nombre_producto", "Desconocido")
                cantidad = item.get("cantidad", 0)
                subtotal = item.get("subtotal", 0)
                
                contador_productos[nombre] += cantidad
                ingresos_por_producto[nombre] += subtotal
        
        # Top 5 productos más vendidos
        productos_mas_vendidos = contador_productos.most_common(5)
        
        # Calcular ventas por categoría
        ventas_por_categoria = Counter()
        for venta in ventas_semana:
            for item in venta.get("items", []):
                id_prod = item.get("id_producto")
                producto = self.productos.obtener_producto(id_prod)
                if producto:
                    ventas_por_categoria[producto.get("categoria", "Sin categoría")] += item.get("cantidad", 0)
        
        # Calcular promedio de venta
        promedio_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
        
        # Productos con stock bajo
        alertas_stock = self.productos.obtener_alertas_stock()
        
        # Construir reporte
        reporte = {
            "periodo": {
                "inicio": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                "fin": datetime.now().strftime("%Y-%m-%d")
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
            "productos_stock_bajo": len(alertas_stock),
            "alertas_stock": [
                {"nombre": p["nombre"], "stock": p["cantidad_stock"]}
                for p in alertas_stock
            ]
        }
        
        return reporte

    def mostrar_reporte_semanal(self):
        """
        Genera y muestra el reporte semanal formateado en consola.
        
        Returns:
            str: Reporte formateado como texto
        """
        reporte = self.reporte_semanal()
        
        linea = "═" * 60
        linea_simple = "─" * 60
        
        texto = f"""
╔{linea}╗
║{'REPORTE SEMANAL - GLAMSTORE':^60}║
║{f"Del {reporte['periodo']['inicio']} al {reporte['periodo']['fin']}":^60}║
╚{linea}╝

📊 RESUMEN GENERAL
{linea_simple}
  📦 Total de ventas realizadas:    {reporte['total_ventas']:>10}
  💰 Total de ingresos:             ${reporte['total_ingresos']:>10,.2f}
  📈 Promedio por venta:            ${reporte['promedio_por_venta']:>10,.2f}
{linea_simple}

🏆 TOP 5 - PRODUCTOS MÁS VENDIDOS
{linea_simple}"""
        
        if reporte['productos_mas_vendidos']:
            for i, prod in enumerate(reporte['productos_mas_vendidos'], 1):
                medalla = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
                texto += f"\n  {medalla} {prod['nombre']:<35} {prod['cantidad']:>5} uds vendidas"
        else:
            texto += "\n  No hay ventas registradas en este período."
        
        texto += f"""
{linea_simple}

💵 TOP 5 - PRODUCTOS QUE MÁS INGRESOS GENERARON
{linea_simple}"""
        
        if reporte['ingresos_por_producto']:
            for i, prod in enumerate(reporte['ingresos_por_producto'], 1):
                texto += f"\n  {i}. {prod['nombre']:<35} ${prod['ingresos']:>10,.2f}"
        else:
            texto += "\n  No hay ingresos registrados en este período."
        
        texto += f"""
{linea_simple}

📂 VENTAS POR CATEGORÍA
{linea_simple}"""
        
        if reporte['ventas_por_categoria']:
            for cat in reporte['ventas_por_categoria']:
                barra = "█" * min(cat['cantidad'], 30)
                texto += f"\n  {cat['categoria']:<20} {barra} ({cat['cantidad']})"
        else:
            texto += "\n  No hay datos de categorías."
        
        texto += f"""
{linea_simple}

⚠️  ALERTAS DE STOCK BAJO ({reporte['productos_stock_bajo']} productos)
{linea_simple}"""
        
        if reporte['alertas_stock']:
            for alerta in reporte['alertas_stock']:
                indicador = "🔴" if alerta['stock'] == 0 else "🟡"
                texto += f"\n  {indicador} {alerta['nombre']:<35} Stock: {alerta['stock']} uds"
        else:
            texto += "\n  ✅ Todos los productos tienen stock suficiente."
        
        texto += f"\n{linea_simple}\n"
        
        return texto

    def estadisticas_generales(self):
        """
        Genera estadísticas generales del inventario.
        
        Returns:
            dict: Estadísticas del inventario
        """
        productos = self.productos.listar_productos()
        
        total_productos = len(productos)
        total_unidades = sum(p["cantidad_stock"] for p in productos)
        valor_inventario = sum(p["precio"] * p["cantidad_stock"] for p in productos)
        
        # Contar por categoría
        categorias = Counter(p["categoria"] for p in productos)
        
        # Precio promedio
        precio_promedio = sum(p["precio"] for p in productos) / total_productos if total_productos > 0 else 0
        
        return {
            "total_productos": total_productos,
            "total_unidades_stock": total_unidades,
            "valor_total_inventario": round(valor_inventario, 2),
            "precio_promedio": round(precio_promedio, 2),
            "productos_por_categoria": dict(categorias),
            "productos_stock_bajo": len(self.productos.obtener_alertas_stock()),
            "productos_sin_stock": len([p for p in productos if p["cantidad_stock"] == 0])
        }

    def mostrar_estadisticas(self):
        """
        Muestra las estadísticas generales formateadas en consola.
        
        Returns:
            str: Estadísticas formateadas como texto
        """
        stats = self.estadisticas_generales()
        
        linea = "─" * 55
        
        texto = f"""
📊 ESTADÍSTICAS GENERALES DEL INVENTARIO
{linea}
  📦 Total de productos registrados:  {stats['total_productos']:>10}
  📋 Total de unidades en stock:      {stats['total_unidades_stock']:>10}
  💎 Valor total del inventario:      ${stats['valor_total_inventario']:>10,.2f}
  💲 Precio promedio de productos:    ${stats['precio_promedio']:>10,.2f}
  ⚠️  Productos con stock bajo:        {stats['productos_stock_bajo']:>10}
  🔴 Productos sin stock:             {stats['productos_sin_stock']:>10}
{linea}

📂 PRODUCTOS POR CATEGORÍA
{linea}"""
        
        for cat, cant in sorted(stats['productos_por_categoria'].items(), key=lambda x: x[1], reverse=True):
            barra = "█" * min(cant, 30)
            texto += f"\n  {cat:<25} {barra} ({cant})"
        
        texto += f"\n{linea}\n"
        
        return texto
