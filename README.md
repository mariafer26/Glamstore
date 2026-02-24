# 💄 GlamStore - Sistema de Gestión para Tienda de Maquillaje

Sistema completo de gestión para una tienda física de maquillaje, desarrollado en **dos fases**: versión en consola (Python puro) y versión web (Flask + SQLite).

---

## 📁 Estructura del Proyecto

```
sistema de gestion/
│
├── README.md                       # Este archivo
│
├── fase1_consola/                  # FASE 1: Versión en consola
│   ├── main.py                     # Punto de entrada principal
│   ├── modulos/                    # Módulos del sistema
│   │   ├── __init__.py            # Inicialización del paquete
│   │   ├── base_datos.py          # Persistencia de datos (JSON)
│   │   ├── productos.py           # Gestión de productos (CRUD)
│   │   ├── ventas.py              # Registro y control de ventas
│   │   └── reportes.py           # Generación de reportes
│   ├── datos/                      # Archivos de datos (auto-generados)
│   │   ├── productos.json
│   │   ├── ventas.json
│   │   └── config.json
│   └── backups/                    # Copias de seguridad
│
├── fase2_web/                      # FASE 2: Versión web con Flask
│   ├── app.py                      # Aplicación Flask principal
│   ├── config.py                   # Configuración de la app
│   ├── models.py                   # Modelos y acceso a BD (SQLite)
│   ├── requirements.txt           # Dependencias Python
│   ├── routes/                     # Rutas organizadas por módulo
│   │   ├── __init__.py
│   │   ├── dashboard.py           # Panel principal
│   │   ├── productos.py           # CRUD de productos
│   │   ├── ventas.py              # Registro de ventas
│   │   └── reportes.py           # Reportes semanales
│   ├── templates/                  # Plantillas HTML (Jinja2)
│   │   ├── base.html              # Plantilla base con sidebar
│   │   ├── dashboard.html         # Panel principal
│   │   ├── productos/
│   │   │   ├── lista.html         # Lista de productos
│   │   │   ├── agregar.html       # Formulario agregar
│   │   │   └── editar.html        # Formulario editar
│   │   ├── ventas/
│   │   │   ├── registrar.html     # Formulario nueva venta
│   │   │   └── historial.html     # Historial de ventas
│   │   └── reportes/
│   │       └── semanal.html       # Reporte semanal
│   └── static/                     # Archivos estáticos
│       ├── css/
│       │   └── styles.css         # Estilos CSS completos
│       └── js/
│           └── app.js             # JavaScript de interacción
```

---

## 🚀 Cómo Ejecutar

### Fase 1: Versión en Consola

```bash
# 1. Navegar al directorio de la fase 1
cd "sistema de gestion/fase1_consola"

# 2. Ejecutar el sistema
python3 main.py
```

> No se requiere instalar dependencias adicionales. Usa Python 3.7+.

### Fase 2: Versión Web con Flask

```bash
# 1. Navegar al directorio de la fase 2
cd "sistema de gestion/fase2_web"

# 2. (Opcional) Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate   # En Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python3 app.py

# 5. Abrir en el navegador
# http://localhost:5000
```

---

## 📋 Funcionalidades

### ✅ Gestión de Productos
- Registrar productos con nombre, marca, categoría, precio y stock
- Listar todos los productos con indicadores visuales de stock
- Buscar productos por nombre o marca
- Editar datos de productos existentes
- Actualizar cantidad en stock
- Eliminar productos (eliminación lógica)
- Filtrar por categoría
- **15 categorías** de maquillaje predefinidas

### ✅ Control de Inventario
- Reducción automática de stock al registrar ventas
- **Alerta visual** cuando el stock es ≤ 5 unidades
- Indicadores de color: 🟢 OK | 🟡 Bajo | 🔴 Sin stock
- Panel de alertas de stock bajo

### ✅ Registro de Ventas
- Registrar ventas con uno o múltiples productos
- Cálculo automático de subtotales y total
- Historial completo de ventas con detalle
- Stock se actualiza automáticamente al vender

### ✅ Reportes Semanales
- Total de ventas realizadas
- Total de ingresos generados
- Promedio por venta
- **Top 5 productos más vendidos**
- **Productos que más ingresos generan**
- Ventas por categoría (con barras visuales)
- Alertas de stock bajo

### ✅ Persistencia de Datos
- **Fase 1**: Archivos JSON (no se pierden datos al cerrar)
- **Fase 2**: Base de datos SQLite
- Sistema de backups automáticos (Fase 1)

### ✅ Interfaz
- **Fase 1**: Menú organizado con emojis y formato visual
- **Fase 2**: Diseño web moderno, dark theme premium, responsive

---

## 🎨 Categorías Disponibles

| # | Categoría |
|---|-----------|
| 1 | Labiales |
| 2 | Bases |
| 3 | Sombras |
| 4 | Rubores |
| 5 | Correctores |
| 6 | Máscaras de pestañas |
| 7 | Delineadores |
| 8 | Polvos |
| 9 | Primers |
| 10 | Brochas y herramientas |
| 11 | Skincare |
| 12 | Perfumes |
| 13 | Uñas |
| 14 | Accesorios |
| 15 | Otro |

---

## 🔧 Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| **Python 3** | Lenguaje principal |
| **Flask** | Framework web (Fase 2) |
| **SQLite** | Base de datos relacional (Fase 2) |
| **JSON** | Persistencia de datos (Fase 1) |
| **HTML5** | Estructura de páginas web |
| **CSS3** | Diseño y estilos (dark theme premium) |
| **JavaScript** | Interactividad del lado del cliente |
| **Jinja2** | Motor de plantillas HTML |
| **Google Fonts** | Tipografía (Inter + Outfit) |

---

## 🚀 Mejoras Futuras Recomendadas

### 📊 Gráficas de Ventas
- Integrar Chart.js o Plotly para gráficas interactivas
- Gráficas de barras, líneas y pastel
- Comparación de ventas por período

### 👥 Control de Usuarios
- Sistema de autenticación (login/registro)
- Roles: Administrador, Vendedor, Supervisor
- Historial de acciones por usuario
- Implementable con Flask-Login

### 📄 Exportar Reportes a PDF
- Generar reportes en formato PDF descargable
- Implementable con weasyprint o ReportLab
- Incluir logo y branding de la tienda

### 💾 Backup Automático
- Programar backups diarios/semanales
- Exportar datos a CSV o Excel
- Sincronización con almacenamiento en la nube

### 🛒 Ventas Online
- Catálogo público de productos
- Carrito de compras
- Pasarela de pagos (Stripe, PayPal, etc.)
- Gestión de envíos

### 📱 App Móvil
- Versión responsive ya preparada
- PWA (Progressive Web App)
- Notificaciones push para alertas de stock

### 🔒 Seguridad
- HTTPS en producción
- Protección CSRF (ya incluida con Flask)
- Validación de entradas en servidor
- Rate limiting

### 📈 Business Intelligence
- Dashboard analítico avanzado
- Predicción de demanda
- Análisis de tendencias estacionales
- KPIs personalizados

---

## 📝 Notas Técnicas

- El sistema usa **eliminación lógica** para productos (se marcan como inactivos en lugar de eliminarlos permanentemente), preservando el historial de ventas.
- La arquitectura está diseñada con **Blueprints de Flask**, facilitando agregar nuevos módulos.
- Los modelos usan **funciones puras** con SQLite directo (sin ORM), manteniendo simplicidad y control total.
- El CSS usa **design tokens** (custom properties) para fácil personalización de colores y tipografía.
- La versión web es **responsive** y funciona en computador, tablet y móvil.

---

## 👩‍💻 Autora

María Fernanda Álvarez Marín

---

*GlamStore © 2026 — Sistema de Gestión para Tienda de Maquillaje*
