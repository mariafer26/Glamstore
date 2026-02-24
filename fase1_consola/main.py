#!/usr/bin/env python3
# ============================================================
# GlamStore - Sistema de Gestión para Tienda de Maquillaje
# Versión: 1.0 (Consola)
# Autor: Sistema de Gestión
# Descripción: Sistema completo para administrar inventario
#              y ventas de una tienda física de maquillaje.
# ============================================================
# Instrucciones de ejecución:
#   python3 main.py
# ============================================================

import os
import sys
from modulos import BaseDatos, GestionProductos, GestionVentas, GeneradorReportes
from modulos.productos import CATEGORIAS_VALIDAS, MARCAS_VALIDAS


def limpiar_pantalla():
    """Limpia la pantalla de la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\n  Presiona Enter para continuar...")


def leer_entero(mensaje, minimo=None, maximo=None):
    """
    Lee un número entero del usuario con validación.
    
    Args:
        mensaje (str): Mensaje a mostrar al usuario
        minimo (int, optional): Valor mínimo aceptado
        maximo (int, optional): Valor máximo aceptado
        
    Returns:
        int: Número entero válido ingresado por el usuario
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"  ❌ El valor debe ser al menos {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ❌ El valor no puede ser mayor a {maximo}.")
                continue
            return valor
        except ValueError:
            print("  ❌ Por favor, ingresa un número válido.")


def leer_decimal(mensaje, minimo=None):
    """
    Lee un número decimal del usuario con validación.
    
    Args:
        mensaje (str): Mensaje a mostrar al usuario
        minimo (float, optional): Valor mínimo aceptado
        
    Returns:
        float: Número decimal válido ingresado por el usuario
    """
    while True:
        try:
            valor = float(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"  ❌ El valor debe ser al menos {minimo}.")
                continue
            return valor
        except ValueError:
            print("  ❌ Por favor, ingresa un número válido.")


def mostrar_banner():
    """Muestra el banner principal de la aplicación."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          💄  G L A M S T O R E  💄                          ║
║                                                              ║
║     Sistema de Gestión - Tienda de Maquillaje               ║
║     Versión 1.0 | Consola                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def mostrar_menu_principal():
    """Muestra el menú principal del sistema."""
    print("""
┌──────────────────────────────────────────────┐
│           📋  MENÚ PRINCIPAL                 │
├──────────────────────────────────────────────┤
│                                              │
│   1. 📦  Gestión de Productos               │
│   2. 🛒  Registrar Venta                    │
│   3. 📜  Historial de Ventas                │
│   4. 📊  Reporte Semanal                    │
│   5. 📈  Estadísticas del Inventario        │
│   6. 💾  Crear Backup de Datos              │
│   7. ⚠️   Ver Alertas de Stock              │
│   0. 🚪  Salir del Sistema                  │
│                                              │
└──────────────────────────────────────────────┘
    """)


def mostrar_menu_productos():
    """Muestra el submenú de gestión de productos."""
    print("""
┌──────────────────────────────────────────────┐
│        📦  GESTIÓN DE PRODUCTOS              │
├──────────────────────────────────────────────┤
│                                              │
│   1. ➕  Registrar nuevo producto            │
│   2. 📋  Listar todos los productos         │
│   3. 🔍  Buscar producto                    │
│   4. ✏️   Editar producto                    │
│   5. 📦  Actualizar stock                   │
│   6. 🗑️   Eliminar producto                  │
│   7. 📂  Filtrar por categoría              │
│   0. ↩️   Volver al menú principal           │
│                                              │
└──────────────────────────────────────────────┘
    """)


# ============================================================
# FUNCIONES DE GESTIÓN DE PRODUCTOS
# ============================================================

def registrar_producto(gestion_prod):
    """Interfaz para registrar un nuevo producto."""
    print("\n  ➕ REGISTRAR NUEVO PRODUCTO")
    print("  " + "─" * 40)
    
    nombre = input("  Nombre del producto: ").strip()
    if not nombre:
        print("  ❌ El nombre es obligatorio.")
        return
    
    # Mostrar marcas disponibles
    gestion_prod.mostrar_marcas()
    num_marca = leer_entero("  Selecciona el número de marca: ", 1, len(MARCAS_VALIDAS))
    marca = MARCAS_VALIDAS[num_marca - 1]
    
    # Mostrar categorías disponibles
    gestion_prod.mostrar_categorias()
    num_cat = leer_entero("  Selecciona el número de categoría: ", 1, len(CATEGORIAS_VALIDAS))
    categoria = CATEGORIAS_VALIDAS[num_cat - 1]
    
    precio = leer_decimal("  Precio de venta ($): ", minimo=0.01)
    cantidad = leer_entero("  Cantidad en stock: ", minimo=0)
    
    # Confirmar datos
    print(f"\n  📝 Confirma los datos del producto:")
    print(f"  {'─' * 40}")
    print(f"  Nombre:    {nombre}")
    print(f"  Marca:     {marca}")
    print(f"  Categoría: {categoria}")
    print(f"  Precio:    ${precio:,.2f}")
    print(f"  Stock:     {cantidad} unidades")
    print(f"  {'─' * 40}")
    
    confirmacion = input("  ¿Registrar este producto? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        resultado = gestion_prod.registrar_producto(nombre, marca, categoria, precio, cantidad)
        print(f"\n  {resultado['mensaje']}")
    else:
        print("  ❌ Registro cancelado.")


def listar_productos(gestion_prod):
    """Muestra la lista completa de productos."""
    productos = gestion_prod.listar_productos()
    
    if not productos:
        print("\n  📭 No hay productos registrados en el inventario.")
        return
    
    print(f"\n  📦 INVENTARIO DE PRODUCTOS ({len(productos)} productos)")
    print("  " + "═" * 100)
    
    for producto in productos:
        print(gestion_prod.formato_tabla_producto(producto))
    
    print("  " + "═" * 100)
    
    # Mostrar resumen
    total_unidades = sum(p["cantidad_stock"] for p in productos)
    valor_total = sum(p["precio"] * p["cantidad_stock"] for p in productos)
    print(f"\n  📊 Total: {len(productos)} productos | {total_unidades} unidades | Valor: ${valor_total:,.2f}")


def buscar_producto(gestion_prod):
    """Busca productos por nombre o marca."""
    termino = input("\n  🔍 Ingresa el término de búsqueda: ").strip()
    
    if not termino:
        print("  ❌ Debes ingresar un término de búsqueda.")
        return
    
    resultados = gestion_prod.buscar_productos(termino)
    
    if not resultados:
        print(f"  📭 No se encontraron productos que coincidan con '{termino}'.")
        return
    
    print(f"\n  🔍 Resultados para '{termino}' ({len(resultados)} encontrados):")
    print("  " + "═" * 100)
    
    for producto in resultados:
        print(gestion_prod.formato_tabla_producto(producto))
    
    print("  " + "═" * 100)


def editar_producto(gestion_prod):
    """Interfaz para editar los datos de un producto."""
    id_producto = leer_entero("\n  ✏️  Ingresa el ID del producto a editar: ", minimo=1)
    
    producto = gestion_prod.obtener_producto(id_producto)
    if not producto:
        print(f"  ❌ No se encontró el producto con ID #{id_producto}.")
        return
    
    print(f"\n  Datos actuales del producto:")
    print(gestion_prod.formato_tabla_producto(producto))
    
    print(f"\n  Ingresa los nuevos datos (deja en blanco para mantener el valor actual):")
    
    datos_nuevos = {}
    
    nombre = input(f"  Nombre [{producto['nombre']}]: ").strip()
    if nombre:
        datos_nuevos["nombre"] = nombre.title()
    
    cambiar_marca = input(f"  ¿Cambiar marca? [{producto['marca']}] (s/n): ").strip().lower()
    if cambiar_marca == 's':
        gestion_prod.mostrar_marcas()
        num_marca = leer_entero("  Selecciona el número de marca: ", 1, len(MARCAS_VALIDAS))
        datos_nuevos["marca"] = MARCAS_VALIDAS[num_marca - 1]
    
    cambiar_cat = input(f"  ¿Cambiar categoría? [{producto['categoria']}] (s/n): ").strip().lower()
    if cambiar_cat == 's':
        gestion_prod.mostrar_categorias()
        num_cat = leer_entero("  Selecciona el número de categoría: ", 1, len(CATEGORIAS_VALIDAS))
        datos_nuevos["categoria"] = CATEGORIAS_VALIDAS[num_cat - 1]
    
    precio_str = input(f"  Precio [${producto['precio']:,.2f}]: ").strip()
    if precio_str:
        try:
            precio = float(precio_str)
            if precio > 0:
                datos_nuevos["precio"] = precio
            else:
                print("  ⚠️  Precio no válido, se mantiene el actual.")
        except ValueError:
            print("  ⚠️  Precio no válido, se mantiene el actual.")
    
    if datos_nuevos:
        resultado = gestion_prod.actualizar_producto(id_producto, datos_nuevos)
        print(f"\n  {resultado['mensaje']}")
    else:
        print("  ℹ️  No se realizaron cambios.")


def actualizar_stock(gestion_prod):
    """Interfaz para actualizar el stock de un producto."""
    id_producto = leer_entero("\n  📦 Ingresa el ID del producto: ", minimo=1)
    
    producto = gestion_prod.obtener_producto(id_producto)
    if not producto:
        print(f"  ❌ No se encontró el producto con ID #{id_producto}.")
        return
    
    print(f"\n  Producto: {producto['nombre']} ({producto['marca']})")
    print(f"  Stock actual: {producto['cantidad_stock']} unidades")
    
    nueva_cantidad = leer_entero("  Nueva cantidad en stock: ", minimo=0)
    
    resultado = gestion_prod.actualizar_stock(id_producto, nueva_cantidad)
    print(f"\n  {resultado['mensaje']}")


def eliminar_producto(gestion_prod):
    """Interfaz para eliminar un producto."""
    id_producto = leer_entero("\n  🗑️  Ingresa el ID del producto a eliminar: ", minimo=1)
    
    producto = gestion_prod.obtener_producto(id_producto)
    if not producto:
        print(f"  ❌ No se encontró el producto con ID #{id_producto}.")
        return
    
    print(f"\n  ⚠️  Vas a eliminar el siguiente producto:")
    print(gestion_prod.formato_tabla_producto(producto))
    
    confirmacion = input("\n  ¿Estás seguro? Esta acción no se puede deshacer (s/n): ").strip().lower()
    
    if confirmacion == 's':
        resultado = gestion_prod.eliminar_producto(id_producto)
        print(f"\n  {resultado['mensaje']}")
    else:
        print("  ❌ Eliminación cancelada.")


def filtrar_por_categoria(gestion_prod):
    """Filtra y muestra productos por categoría."""
    gestion_prod.mostrar_categorias()
    num_cat = leer_entero("  Selecciona el número de categoría: ", 1, len(CATEGORIAS_VALIDAS))
    categoria = CATEGORIAS_VALIDAS[num_cat - 1]
    
    productos = gestion_prod.listar_productos(filtro_categoria=categoria)
    
    if not productos:
        print(f"\n  📭 No hay productos en la categoría '{categoria}'.")
        return
    
    print(f"\n  📂 Productos en '{categoria}' ({len(productos)})")
    print("  " + "═" * 100)
    
    for producto in productos:
        print(gestion_prod.formato_tabla_producto(producto))
    
    print("  " + "═" * 100)


# ============================================================
# FUNCIONES DE GESTIÓN DE VENTAS
# ============================================================

def registrar_venta(gestion_ventas, gestion_prod):
    """
    Interfaz para registrar una nueva venta.
    Permite agregar múltiples productos a la misma venta.
    """
    print("\n  🛒 REGISTRAR NUEVA VENTA")
    print("  " + "─" * 40)
    
    # Mostrar productos disponibles
    productos = gestion_prod.listar_productos()
    if not productos:
        print("  📭 No hay productos registrados para vender.")
        return
    
    print("\n  Productos disponibles:")
    print("  " + "═" * 100)
    for producto in productos:
        if producto["cantidad_stock"] > 0:
            print(gestion_prod.formato_tabla_producto(producto))
    print("  " + "═" * 100)
    
    items_venta = []
    
    while True:
        print(f"\n  📦 Producto #{len(items_venta) + 1} de la venta")
        id_producto = leer_entero("  ID del producto: ", minimo=1)
        
        producto = gestion_prod.obtener_producto(id_producto)
        if not producto:
            print(f"  ❌ No se encontró el producto con ID #{id_producto}.")
            continue
        
        if not producto.get("activo", True):
            print(f"  ❌ El producto '{producto['nombre']}' no está disponible.")
            continue
        
        print(f"  → {producto['nombre']} ({producto['marca']}) | Stock: {producto['cantidad_stock']} | ${producto['precio']:,.2f}")
        
        cantidad = leer_entero("  Cantidad a vender: ", minimo=1)
        
        if cantidad > producto["cantidad_stock"]:
            print(f"  ❌ Stock insuficiente. Disponible: {producto['cantidad_stock']} unidades.")
            continue
        
        items_venta.append({
            "id_producto": id_producto,
            "cantidad": cantidad
        })
        
        print(f"  ✅ {producto['nombre']} × {cantidad} agregado a la venta.")
        
        agregar_mas = input("\n  ¿Agregar otro producto a la venta? (s/n): ").strip().lower()
        if agregar_mas != 's':
            break
    
    if not items_venta:
        print("  ❌ Venta cancelada. No se agregaron productos.")
        return
    
    # Confirmar venta
    print("\n  📝 Resumen de la venta:")
    print("  " + "─" * 40)
    total_estimado = 0
    for item in items_venta:
        producto = gestion_prod.obtener_producto(item["id_producto"])
        subtotal = producto["precio"] * item["cantidad"]
        total_estimado += subtotal
        print(f"  • {producto['nombre']} × {item['cantidad']} = ${subtotal:,.2f}")
    print("  " + "─" * 40)
    print(f"  💰 Total estimado: ${total_estimado:,.2f}")
    
    confirmacion = input("\n  ¿Confirmar la venta? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        resultado = gestion_ventas.registrar_venta(items_venta)
        print(resultado['mensaje'])
    else:
        print("  ❌ Venta cancelada.")


def ver_historial_ventas(gestion_ventas):
    """Muestra el historial de ventas."""
    print("\n  📜 HISTORIAL DE VENTAS")
    
    # Preguntar cuántas ventas mostrar
    print("  1. Últimas 5 ventas")
    print("  2. Últimas 10 ventas")
    print("  3. Últimas 20 ventas")
    print("  4. Todas las ventas")
    
    opcion = leer_entero("  Selecciona una opción: ", 1, 4)
    limites = {1: 5, 2: 10, 3: 20, 4: None}
    limite = limites[opcion]
    
    ventas = gestion_ventas.obtener_historial(limite=limite)
    
    if not ventas:
        print("\n  📭 No hay ventas registradas.")
        return
    
    print(f"\n  📜 Mostrando {len(ventas)} venta(s)")
    print("  " + "═" * 55)
    
    for venta in ventas:
        print(gestion_ventas.formato_venta(venta))
    
    print("  " + "═" * 55)
    
    # Mostrar total
    total = sum(v.get("total", 0) for v in ventas)
    print(f"\n  💰 Total mostrado: ${total:,.2f}")


# ============================================================
# FUNCIONES DE REPORTES
# ============================================================

def ver_reporte_semanal(reportes):
    """Muestra el reporte semanal."""
    print(reportes.mostrar_reporte_semanal())


def ver_estadisticas(reportes):
    """Muestra las estadísticas generales del inventario."""
    print(reportes.mostrar_estadisticas())


# ============================================================
# FUNCIONES ADICIONALES
# ============================================================

def crear_backup(db):
    """Crea un backup de los datos."""
    print("\n  💾 CREAR BACKUP DE DATOS")
    print("  " + "─" * 40)
    
    confirmacion = input("  ¿Deseas crear una copia de seguridad? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        ruta = db.crear_backup()
        if ruta:
            print(f"\n  ✅ Backup creado exitosamente en:")
            print(f"  📁 {ruta}")
        else:
            print("  ❌ Error al crear el backup.")
    else:
        print("  ❌ Backup cancelado.")


def ver_alertas_stock(gestion_prod):
    """Muestra las alertas de stock bajo."""
    alertas = gestion_prod.obtener_alertas_stock()
    
    print("\n  ⚠️  ALERTAS DE STOCK BAJO")
    print("  " + "─" * 50)
    
    if not alertas:
        print("  ✅ ¡Excelente! Todos los productos tienen stock suficiente.")
        return
    
    print(f"  Se encontraron {len(alertas)} producto(s) con stock bajo (≤ 5 unidades):\n")
    
    for producto in alertas:
        indicador = "🔴" if producto["cantidad_stock"] == 0 else "🟡"
        print(f"  {indicador} #{producto['id']:03d} | {producto['nombre']:<25} | "
              f"Marca: {producto['marca']:<15} | Stock: {producto['cantidad_stock']} unidades")
    
    print("\n  💡 Consejo: Reabastecer estos productos lo antes posible.")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """
    Función principal del sistema.
    Inicializa los módulos y ejecuta el bucle del menú principal.
    """
    # Inicializar módulos
    db = BaseDatos()
    gestion_prod = GestionProductos(db)
    gestion_ventas = GestionVentas(db, gestion_prod)
    reportes = GeneradorReportes(db, gestion_prod, gestion_ventas)
    
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        # Verificar alertas de stock
        alertas = gestion_prod.obtener_alertas_stock()
        if alertas:
            print(f"  ⚠️  ¡Atención! {len(alertas)} producto(s) con stock bajo.\n")
        
        mostrar_menu_principal()
        
        opcion = input("  👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            # Submenú de productos
            while True:
                limpiar_pantalla()
                mostrar_banner()
                mostrar_menu_productos()
                
                sub_opcion = input("  👉 Selecciona una opción: ").strip()
                
                if sub_opcion == "1":
                    registrar_producto(gestion_prod)
                elif sub_opcion == "2":
                    listar_productos(gestion_prod)
                elif sub_opcion == "3":
                    buscar_producto(gestion_prod)
                elif sub_opcion == "4":
                    editar_producto(gestion_prod)
                elif sub_opcion == "5":
                    actualizar_stock(gestion_prod)
                elif sub_opcion == "6":
                    eliminar_producto(gestion_prod)
                elif sub_opcion == "7":
                    filtrar_por_categoria(gestion_prod)
                elif sub_opcion == "0":
                    break
                else:
                    print("  ❌ Opción no válida.")
                
                pausar()
        
        elif opcion == "2":
            registrar_venta(gestion_ventas, gestion_prod)
            pausar()
        
        elif opcion == "3":
            ver_historial_ventas(gestion_ventas)
            pausar()
        
        elif opcion == "4":
            ver_reporte_semanal(reportes)
            pausar()
        
        elif opcion == "5":
            ver_estadisticas(reportes)
            pausar()
        
        elif opcion == "6":
            crear_backup(db)
            pausar()
        
        elif opcion == "7":
            ver_alertas_stock(gestion_prod)
            pausar()
        
        elif opcion == "0":
            print("\n  👋 ¡Gracias por usar GlamStore!")
            print("  💄 ¡Hasta pronto!\n")
            sys.exit(0)
        
        else:
            print("  ❌ Opción no válida. Intenta de nuevo.")
            pausar()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
