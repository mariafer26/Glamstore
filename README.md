<div align="center">

# 💄 GlamStore

### Sistema de Gestión para Tienda de Maquillaje

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

> ✨ Sistema completo de gestión para una tienda de maquillaje, desarrollado en **dos fases**: versión en consola (Python puro) y versión web con interfaz dark premium (Flask + SQLite).

</div>

---

## 🌟 ¿Qué es GlamStore?

**GlamStore** es una solución de gestión empresarial diseñada especialmente para tiendas de maquillaje y belleza. Permite controlar el inventario, registrar ventas, generar reportes y mantener un historial completo de operaciones — todo desde una interfaz elegante y fácil de usar.

---

## 📸 Vista Previa

| 🖥️ Fase 1 — Consola | 🌐 Fase 2 — Web |
|:---:|:---:|
| Menú interactivo en terminal | Dashboard web con dark theme premium |
| Sin dependencias externas | Flask + SQLite + diseño responsive |

---

## ⚡ Inicio Rápido

### 🖥️ Fase 1 — Versión Consola

```bash
# Navegar al directorio
cd fase1_consola

# Ejecutar (requiere Python 3.7+, sin dependencias adicionales)
python3 main.py
```

### 🌐 Fase 2 — Versión Web

```bash
# Navegar al directorio
cd fase2_web

# Crear y activar entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate       # macOS / Linux
# venv\Scripts\activate        # Windows

# Instalar dependencias
pip install -r requirements.txt

# Lanzar la aplicación
python3 app.py
```

🔗 Abrir en el navegador: **http://localhost:5000**

---

## ✨ Funcionalidades Principales

<table>
  <tr>
    <td valign="top" width="50%">

### 📦 Gestión de Productos
- Registrar con nombre, marca, categoría, precio y stock
- Buscar por nombre o marca
- Editar y eliminar (eliminación lógica)
- Filtrar por categoría
- **15 categorías** predefinidas de maquillaje

### 📊 Control de Inventario
- Reducción automática de stock al vender
- Alerta visual cuando el stock es ≤ 5 unidades
- Indicadores: 🟢 OK · 🟡 Bajo · 🔴 Sin stock
- Panel dedicado de alertas

    </td>
    <td valign="top" width="50%">

### 🛍️ Registro de Ventas
- Ventas con uno o múltiples productos
- Cálculo automático de subtotales y total
- Historial completo con detalle
- Stock actualizado en tiempo real

### 📈 Reportes Semanales
- Total de ventas e ingresos generados
- Promedio por venta
- 🏆 Top 5 productos más vendidos
- Ventas por categoría (con barras visuales)
- Alertas de stock bajo integradas

    </td>
  </tr>
</table>

---

## 🎨 Categorías de Maquillaje

<div align="center">

| 💋 Labiales | 🧴 Bases | 👁️ Sombras | 🌸 Rubores | 🎭 Correctores |
|:-----------:|:--------:|:----------:|:----------:|:--------------:|
| Máscaras de pestañas | Delineadores | Polvos | Primers | Brochas y herramientas |
| Skincare | Perfumes | Uñas | Accesorios | Otro |

</div>

---

## 🗂️ Estructura del Proyecto

```
Glamstore/
│
├── 📄 README.md
│
├── 🖥️ fase1_consola/               # FASE 1: Versión en consola
│   ├── main.py                     # Punto de entrada
│   ├── modulos/
│   │   ├── base_datos.py           # Persistencia JSON
│   │   ├── productos.py            # CRUD de productos
│   │   ├── ventas.py               # Control de ventas
│   │   └── reportes.py             # Generación de reportes
│   ├── datos/                      # JSON auto-generados
│   └── backups/                    # Copias de seguridad
│
└── 🌐 fase2_web/                   # FASE 2: Versión web Flask
    ├── app.py                      # Aplicación principal
    ├── config.py                   # Configuración
    ├── models.py                   # Modelos SQLite
    ├── requirements.txt            # Dependencias
    ├── routes/                     # Blueprints por módulo
    │   ├── dashboard.py
    │   ├── productos.py
    │   ├── ventas.py
    │   └── reportes.py
    ├── templates/                  # Plantillas Jinja2
    │   ├── base.html               # Layout con sidebar
    │   ├── dashboard.html
    │   ├── productos/
    │   ├── ventas/
    │   └── reportes/
    └── static/
        ├── css/styles.css          # Dark theme premium
        └── js/app.js               # Interactividad
```

---

## 🔧 Stack Tecnológico

| Tecnología | Versión | Rol |
|:----------:|:-------:|:---:|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.7+ | Lenguaje principal |
| ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white) | 2.x | Framework web (Fase 2) |
| ![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white) | 3 | Base de datos (Fase 2) |
| ![JSON](https://img.shields.io/badge/-JSON-000000?logo=json&logoColor=white) | — | Persistencia (Fase 1) |
| ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white) | 5 | Estructura web |
| ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white) | 3 | Estilos y dark theme |
| ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black) | ES6+ | Interactividad |
| ![Jinja2](https://img.shields.io/badge/-Jinja2-B41717?logo=jinja&logoColor=white) | — | Motor de plantillas |
| ![Google Fonts](https://img.shields.io/badge/-Google%20Fonts-4285F4?logo=google&logoColor=white) | — | Inter + Outfit |

---

## 🚀 Roadmap — Mejoras Futuras

- [ ] 📊 **Gráficas interactivas** con Chart.js o Plotly
- [ ] 👥 **Sistema de usuarios** con roles (Admin, Vendedor, Supervisor) vía Flask-Login
- [ ] 📄 **Exportar reportes a PDF** con weasyprint o ReportLab
- [ ] 💾 **Backups automáticos** programados y exportación a CSV/Excel
- [ ] 🛒 **Tienda online** con catálogo público y pasarela de pagos
- [ ] 📱 **PWA** (Progressive Web App) con notificaciones push
- [ ] 🔒 **Seguridad avanzada**: HTTPS, rate limiting, validación de entradas
- [ ] 📈 **Business Intelligence**: predicción de demanda y KPIs personalizados

---

## 📝 Notas Técnicas

> 💡 **Eliminación lógica**: los productos se marcan como inactivos en vez de borrarse, preservando el historial de ventas.

> 🏗️ **Arquitectura Blueprints**: diseño modular que facilita agregar nuevos módulos sin afectar el código existente.

> 🎨 **Design Tokens**: el CSS utiliza custom properties para personalización sencilla de colores y tipografía.

> 📱 **Responsive**: la versión web se adapta a computador, tablet y móvil.

---

## 👩‍💻 Autora

<div align="center">

**María Fernanda Álvarez Marín**

*Desarrolladora Full Stack · Apasionada por el diseño y la tecnología*

</div>

---

<div align="center">

*💄 GlamStore © 2026 — Hecho con ❤️ para el mundo de la belleza*

</div>
