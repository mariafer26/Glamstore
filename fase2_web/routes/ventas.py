# ============================================================
# Rutas del Módulo de Ventas
# ============================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import obtener_productos, obtener_producto_por_id, registrar_venta, obtener_ventas, obtener_venta_por_id
from config import Config

# Crear blueprint para ventas
ventas_bp = Blueprint('ventas', __name__, url_prefix='/ventas')


@ventas_bp.route('/')
def historial():
    """Muestra el historial de ventas."""
    ventas = obtener_ventas(limite=50)
    
    total_mostrado = sum(v.get("total", 0) for v in ventas)
    
    return render_template(
        'ventas/historial.html',
        ventas=ventas,
        total_mostrado=round(total_mostrado, 2)
    )


@ventas_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Formulario para registrar una nueva venta."""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            productos_ids = request.form.getlist('producto_id[]')
            cantidades = request.form.getlist('cantidad[]')
            
            if not productos_ids or not cantidades:
                flash('Debes agregar al menos un producto a la venta.', 'error')
                productos = obtener_productos()
                return render_template('ventas/registrar.html', productos=productos)
            
            # Construir lista de items
            items = []
            for i in range(len(productos_ids)):
                if productos_ids[i] and cantidades[i]:
                    producto_id = int(productos_ids[i])
                    cantidad = int(cantidades[i])
                    
                    if cantidad > 0:
                        items.append({
                            "producto_id": producto_id,
                            "cantidad": cantidad
                        })
            
            if not items:
                flash('No se agregaron productos válidos a la venta.', 'error')
                productos = obtener_productos()
                return render_template('ventas/registrar.html', productos=productos)
            
            # Registrar la venta
            resultado = registrar_venta(items)
            
            if resultado["exito"]:
                flash(f'¡Venta #{resultado["venta_id"]} registrada! Total: ${resultado["total"]:,.2f}', 'success')
                
                # Mostrar alertas de stock
                for alerta in resultado.get("alertas", []):
                    flash(f'⚠️ Stock bajo: {alerta["nombre"]} ({alerta["stock"]} unidades)', 'warning')
                
                return redirect(url_for('ventas.detalle', venta_id=resultado["venta_id"]))
            else:
                flash(resultado.get("mensaje", "Error al registrar la venta."), 'error')
        
        except (ValueError, KeyError) as e:
            flash(f'Error en los datos: {str(e)}', 'error')
    
    productos = obtener_productos()
    # Filtrar solo productos con stock disponible
    productos_disponibles = [p for p in productos if p["cantidad_stock"] > 0]
    
    return render_template('ventas/registrar.html', productos=productos_disponibles)


@ventas_bp.route('/detalle/<int:venta_id>')
def detalle(venta_id):
    """Muestra el detalle de una venta específica."""
    venta = obtener_venta_por_id(venta_id)
    
    if not venta:
        flash('Venta no encontrada.', 'error')
        return redirect(url_for('ventas.historial'))
    
    return render_template('ventas/historial.html', ventas=[venta], venta_detalle=venta, total_mostrado=venta["total"])


@ventas_bp.route('/api/producto/<int:producto_id>')
def api_producto(producto_id):
    """API endpoint para obtener datos de un producto (usado por JavaScript)."""
    producto = obtener_producto_por_id(producto_id)
    
    if producto:
        return jsonify({
            "id": producto["id"],
            "nombre": producto["nombre"],
            "marca": producto["marca"],
            "precio": producto["precio"],
            "stock": producto["cantidad_stock"]
        })
    
    return jsonify({"error": "Producto no encontrado"}), 404
