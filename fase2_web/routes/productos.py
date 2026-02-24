# ============================================================
# Rutas del Módulo de Productos
# ============================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import (
    obtener_productos, obtener_producto_por_id,
    crear_producto, actualizar_producto, eliminar_producto
)
from config import Config

# Crear blueprint para productos
productos_bp = Blueprint('productos', __name__, url_prefix='/productos')


@productos_bp.route('/')
def lista():
    """Lista todos los productos del inventario."""
    categoria = request.args.get('categoria', None)
    stock_bajo = request.args.get('stock_bajo', False)
    
    if stock_bajo:
        productos = obtener_productos(stock_bajo=True)
        titulo = "Productos con Stock Bajo"
    elif categoria:
        productos = obtener_productos(categoria=categoria)
        titulo = f"Productos - {categoria}"
    else:
        productos = obtener_productos()
        titulo = "Todos los Productos"
    
    return render_template(
        'productos/lista.html',
        productos=productos,
        titulo=titulo,
        categorias=Config.CATEGORIAS,
        categoria_actual=categoria,
        stock_minimo=Config.STOCK_MINIMO
    )


@productos_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    """Formulario para agregar un nuevo producto."""
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            marca = request.form.get('marca', '').strip()
            categoria = request.form.get('categoria', '')
            precio = float(request.form.get('precio', 0))
            cantidad = int(request.form.get('cantidad_stock', 0))
            
            # Validaciones
            if not nombre:
                flash('El nombre del producto es obligatorio.', 'error')
                return render_template('productos/agregar.html', categorias=Config.CATEGORIAS)
            
            if marca not in Config.MARCAS:
                flash('Selecciona una marca válida.', 'error')
                return render_template('productos/agregar.html', categorias=Config.CATEGORIAS, marcas=Config.MARCAS)
            
            if categoria not in Config.CATEGORIAS:
                flash('Selecciona una categoría válida.', 'error')
                return render_template('productos/agregar.html', categorias=Config.CATEGORIAS)
            
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'error')
                return render_template('productos/agregar.html', categorias=Config.CATEGORIAS)
            
            if cantidad < 0:
                flash('La cantidad no puede ser negativa.', 'error')
                return render_template('productos/agregar.html', categorias=Config.CATEGORIAS, marcas=Config.MARCAS)
            
            # Crear producto
            producto_id = crear_producto(nombre, marca, categoria, precio, cantidad)
            
            flash(f'¡Producto "{nombre}" registrado exitosamente! (ID: #{producto_id})', 'success')
            
            if cantidad <= Config.STOCK_MINIMO:
                flash(f'⚠️ Atención: El stock inicial es bajo ({cantidad} unidades).', 'warning')
            
            return redirect(url_for('productos.lista'))
            
        except ValueError:
            flash('Por favor, verifica que los datos numéricos sean correctos.', 'error')
    
    return render_template('productos/agregar.html', categorias=Config.CATEGORIAS, marcas=Config.MARCAS)


@productos_bp.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar(producto_id):
    """Formulario para editar un producto existente."""
    producto = obtener_producto_por_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos.lista'))
    
    if request.method == 'POST':
        try:
            datos = {}
            
            nombre = request.form.get('nombre', '').strip()
            if nombre:
                datos['nombre'] = nombre.title()
            
            marca = request.form.get('marca', '').strip()
            if marca and marca in Config.MARCAS:
                datos['marca'] = marca
            
            categoria = request.form.get('categoria', '')
            if categoria and categoria in Config.CATEGORIAS:
                datos['categoria'] = categoria
            
            precio = request.form.get('precio', '')
            if precio:
                precio = float(precio)
                if precio > 0:
                    datos['precio'] = round(precio, 2)
                else:
                    flash('El precio debe ser mayor a 0.', 'error')
                    return render_template('productos/editar.html', producto=producto, categorias=Config.CATEGORIAS)
            
            cantidad = request.form.get('cantidad_stock', '')
            if cantidad != '':
                cantidad = int(cantidad)
                if cantidad >= 0:
                    datos['cantidad_stock'] = cantidad
                else:
                    flash('La cantidad no puede ser negativa.', 'error')
                    return render_template('productos/editar.html', producto=producto, categorias=Config.CATEGORIAS)
            
            if datos:
                actualizar_producto(producto_id, datos)
                flash(f'Producto "{producto["nombre"]}" actualizado correctamente.', 'success')
                
                if datos.get('cantidad_stock', producto['cantidad_stock']) <= Config.STOCK_MINIMO:
                    flash('⚠️ Atención: El stock es bajo.', 'warning')
            else:
                flash('No se realizaron cambios.', 'info')
            
            return redirect(url_for('productos.lista'))
            
        except ValueError:
            flash('Por favor, verifica los datos ingresados.', 'error')
    
    return render_template('productos/editar.html', producto=producto, categorias=Config.CATEGORIAS, marcas=Config.MARCAS)


@productos_bp.route('/eliminar/<int:producto_id>', methods=['POST'])
def eliminar(producto_id):
    """Elimina (desactiva) un producto."""
    producto = obtener_producto_por_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos.lista'))
    
    eliminar_producto(producto_id)
    flash(f'Producto "{producto["nombre"]}" eliminado del inventario.', 'success')
    
    return redirect(url_for('productos.lista'))
