# Referencia del Generador de PDF - ReportLab

## Tabla de Contenidos
1. [Configuración General](#configuración-general)
2. [Tamaños y Márgenes](#tamaños-y-márgenes)
3. [Estilos de Texto](#estilos-de-texto)
4. [Estructura de Tabla](#estructura-de-tabla)
5. [Colores y Diseño](#colores-y-diseño)
6. [Paginación](#paginación)
7. [Ejemplo Completo](#ejemplo-completo)

---

## Configuración General

### Imports necesarios
```python
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
```

### Creación del Documento
```python
# Crear respuesta HTTP para PDF
response = HttpResponse(content_type='application/pdf')
response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

# Crear documento con orientación horizontal
doc = SimpleDocTemplate(
    response, 
    pagesize=landscape(letter),
    leftMargin=0.5*inch,
    rightMargin=0.5*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch
)

# Lista de elementos a agregar al PDF
elements = []
```

---

## Tamaños y Márgenes

### Página
- **Orientación**: Horizontal (`landscape(letter)`)
- **Tamaño base**: Letter (11" × 8.5")
- **Con landscape**: 11" de ancho × 8.5" de alto

### Márgenes
```python
leftMargin=0.5*inch       # 0.5 pulgadas = ~1.27 cm
rightMargin=0.5*inch      # Mínimos para aprovechar espacio
topMargin=0.5*inch
bottomMargin=0.5*inch
```

### Unidades
- `inch` = 1 pulgada = 72 puntos = 2.54 cm
- Típicamente se usa `inch` para márgenes y espacios grandes
- Puntos (pt) para tamaños de fuente

### Ancho de Columnas (importante)
```python
colWidths=[40, 35, 200, 70, 35, 70, 30, 40, 50, 50, 50, 50]
# Total: ~752 puntos (ancho máximo disponible en landscape)

# Desglose para 12 columnas:
# Codigo:     40 pt
# Depto:      35 pt
# Nombre:     200 pt   (columna más ancha)
# Fecha:      70 pt
# Turno:      35 pt
# Horario:    70 pt
# C:          30 pt
# Mov:        40 pt
# Checada1:   50 pt
# Checada2:   50 pt
# Checada3:   50 pt
# Checada4:   50 pt
```

**Nota**: El nombre es la columna más ancha (200 pt) para nombres largos

---

## Estilos de Texto

### Obtener estilos base
```python
styles = getSampleStyleSheet()
# Estilos disponibles: 'Normal', 'Heading1', 'Heading2', 'BodyText', etc.
```

### Estilo personalizado para títulos
```python
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Normal'],
    fontSize=12,              # Tamaño: 12 pt
    alignment=1,              # 1 = Centrado (0=Izq, 1=Cent, 2=Der)
    spaceAfter=10,           # Espacio después: 10 pt
    spaceBefore=10           # Espacio antes: 10 pt
)
```

### Estilo para información de página
```python
ParagraphStyle('PageInfo', 
    fontSize=8,
    alignment=2              # 2 = Alineado a la derecha
)
```

### Tamaños de Fuente usados
- **Títulos**: 12 pt
- **Encabezados de tabla**: 8 pt
- **Datos de tabla**: 7 pt
- **Información adicional**: 8 pt

---

## Estructura de Tabla

### Encabezados de Columnas
```python
headers = [
    'Codigo',      # Número empleado
    'Depto.',      # ID del departamento
    'Nombre',      # Nombre completo
    'Fecha',       # Fecha en formato "Vie 01-08-2024"
    'Turno',       # ID del horario/turno
    'Horario',     # Horario de entrada-salida (ej: 08:00-17:00)
    'C',           # Código de incidencia (A, F, R+, R-, O, ST)
    'Mov',         # Nomenclatura de movimiento
    'Checada1',    # Primera entrada
    'Checada2',    # Primera salida
    'Checada3',    # Segunda entrada
    'Checada4'     # Segunda salida
]
```

### Formato de Datos
```python
row = [
    str(registro.trabajador.numero_empleado),  # "001234"
    str(registro.trabajador.departamento.id),  # "5"
    registro.trabajador.nombre_completo,       # "Juan Pérez García"
    formatear_fecha_espanol(registro.fecha),   # "Vie 01-08-2024"
    str(registro.horario_asignado.id),         # "3"
    horario_str,                               # "08:00-17:00" o "08:00-12:00\n13:00-17:00"
    registro.codigo_incidencia or "",          # "R+" o ""
    registro.movimiento or "",                 # Código de movimiento o vacío
    "08:15",                                   # Hora de checada
    "17:05",
    "12:10",
    "13:00"
]
```

### Construcción de la Tabla
```python
data = [headers]  # Primera fila: encabezados

for registro in registros:
    # ... preparar datos ...
    data.append(row)

# Crear tabla con ancho específico de columnas
table = Table(data, colWidths=[40, 35, 200, 70, 35, 70, 30, 40, 50, 50, 50, 50])
```

---

## Colores y Diseño

### Paleta de Colores
- **Fondo**: `colors.white` (blanco)
- **Texto**: `colors.black` (negro)
- **Bordes**: `colors.black` con espesor 0.5 pt

### Aplicar estilos a tabla
```python
table.setStyle(TableStyle([
    # ENCABEZADOS
    ('BACKGROUND', (0, 0), (-1, 0), colors.white),    # Fondo blanco
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),     # Texto negro
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),            # Alineación
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente negrita
    ('FONTSIZE', (0, 0), (-1, 0), 8),                 # Tamaño 8 pt
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),           # Padding inferior
    ('TOPPADDING', (0, 0), (-1, 0), 8),              # Padding superior
    
    # DATOS
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),      # Fuente normal
    ('FONTSIZE', (0, 1), (-1, -1), 7),                # Tamaño 7 pt
    ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ('TOPPADDING', (0, 1), (-1, -1), 4),
    
    # BORDES
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),   # Grid en toda la tabla
    ('BOX', (0, 0), (-1, -1), 1, colors.black),      # Borde exterior más grueso
    
    # ALINEACIÓN POR COLUMNA
    ('ALIGN', (0, 0), (0, -1), 'CENTER'),   # Codigo - Centro
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),   # Depto - Centro
    ('ALIGN', (2, 0), (2, -1), 'LEFT'),     # Nombre - Izquierda
    ('ALIGN', (3, 0), (3, -1), 'CENTER'),   # Fecha - Centro
    ('ALIGN', (4, 0), (4, -1), 'CENTER'),   # Turno - Centro
    ('ALIGN', (5, 0), (5, -1), 'CENTER'),   # Horario - Centro
    ('ALIGN', (6, 0), (6, -1), 'CENTER'),   # C - Centro
    ('ALIGN', (7, 0), (7, -1), 'CENTER'),   # Mov - Centro
    ('ALIGN', (8, 0), (11, -1), 'CENTER'),  # Checadas - Centro
]))
```

### Fuentes disponibles
- `'Helvetica'` - Fuente estándar sin serif
- `'Helvetica-Bold'` - Helvetica en negrita
- `'Times-Roman'` - Fuente con serif
- Otras: `'Courier'`, `'Times-Bold'`, etc.

---

## Paginación

### Registros por página
```python
registros_por_pagina = 15  # Aproximadamente 15 filas de datos
```

### Estructura de paginación
```python
for i in range(0, total_registros, registros_por_pagina):
    # Obtener lote de registros
    lote_registros = registros_lista[i:i + registros_por_pagina]
    
    # ... crear tabla con lote ...
    
    # Agregar tabla a elementos
    elements.append(table)
    
    # Agregar información de página
    elements.append(Spacer(1, 10))  # Espacio vertical
    elements.append(Paragraph(f"HOJA #{pagina_actual}", ParagraphStyle(...)))
    
    # Agregar salto de página si no es la última
    if i + registros_por_pagina < total_registros:
        elements.append(PageBreak())
        pagina_actual += 1
```

### Encabezado por página
```python
def crear_encabezado_pagina():
    encabezado = []
    encabezado.append(
        Paragraph("TECNOLÓGICO NACIONAL DE MEXICO CAMPUS MINATITLÁN", title_style)
    )
    encabezado.append(
        Paragraph("REGISTRO DE CHECADAS", title_style)
    )
    encabezado.append(
        Paragraph(f"PERIODO DEL {fecha_inicio} AL {fecha_fin}", title_style)
    )
    encabezado.append(
        Paragraph(f"Fecha: {datetime.now().strftime('%d-%m-%Y')}", title_style)
    )
    encabezado.append(Spacer(1, 10))  # Espacio después del encabezado
    return encabezado
```

---

## Ejemplo Completo

```python
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

def generar_reporte_pdf(request):
    """Genera reporte PDF de bitácora"""
    
    # Crear respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registro_checadas.pdf"'
    
    # Crear documento
    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(letter),
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=1,
        spaceAfter=10,
        spaceBefore=10
    )
    
    # Encabezado
    elements.append(Paragraph("TECNOLÓGICO NACIONAL DE MEXICO", title_style))
    elements.append(Paragraph("REGISTRO DE CHECADAS", title_style))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d-%m-%Y')}", title_style))
    elements.append(Spacer(1, 10))
    
    # Datos de tabla
    headers = ['Codigo', 'Depto.', 'Nombre', 'Fecha', 'Turno', 'Horario', 'C', 'Mov', 'Checada1', 'Checada2', 'Checada3', 'Checada4']
    data = [headers]
    
    # Agregar datos (ejemplo)
    data.append(['001234', '5', 'Juan Pérez García', 'Vie 01-08-2024', '3', '08:00-17:00', '', '', '08:15', '17:05', '', ''])
    data.append(['001235', '5', 'María López', 'Vie 01-08-2024', '3', '08:00-17:00', 'R+', '', '08:45', '17:15', '', ''])
    
    # Crear tabla
    table = Table(data, colWidths=[40, 35, 200, 70, 35, 70, 30, 40, 50, 50, 50, 50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('ALIGN', (3, 0), (11, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Construir PDF
    doc.build(elements)
    return response
```

---

## Resumen de Valores Críticos

| Parámetro | Valor | Notas |
|-----------|-------|-------|
| Tamaño página | `landscape(letter)` | 11" × 8.5" |
| Márgenes | `0.5*inch` | Todos los lados |
| Registros/página | 15 filas | Máximo antes de salto |
| Tamaño fuente (títulos) | 12 pt | Centrado |
| Tamaño fuente (encab.) | 8 pt | Helvetica Bold |
| Tamaño fuente (datos) | 7 pt | Helvetica normal |
| Ancho columna (Nombre) | 200 pt | La más ancha |
| Espesor bordes | 0.5 pt (grid), 1 pt (box) | Black |
| Colores | Blanco y Negro | Impresión en B/N |
| Padding encabezado | 8 pt | Arriba/abajo |
| Padding datos | 4 pt | Arriba/abajo |

---

## Tips de Implementación

1. **Horarios Mixtos**: Usar `\n` para separar dos turnos en la misma celda
   ```python
   horario_str = "08:00-12:00\n13:00-17:00"  # Turno de mañana y tarde
   ```

2. **Fechas en Español**: Crear función `formatear_fecha_espanol()` que retorne "Vie 01-08-2024"
   ```python
   from datetime import datetime
   dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sab', 'Dom']
   fecha_str = f"{dias[fecha.weekday()]} {fecha.strftime('%d-%m-%Y')}"
   ```

3. **Espaciado**: Usar `Spacer(1, 10)` para agregar espacios verticales (1 ancho, 10 alto)

4. **Saltos de Página**: `PageBreak()` fuerza nueva página

5. **Alineación Numérica**:
   - 0 = Izquierda
   - 1 = Centrado
   - 2 = Derecha

6. **Rango de tuplas**: `(inicio_col, inicio_fila)` a `(fin_col, fin_fila)`
   - `(0, 0)` = esquina superior izquierda
   - `(-1, -1)` = esquina inferior derecha (último elemento)
   - `(-1, 0)` = toda la primera fila

7. **Construcción incremental**: Agregar elementos a `elements[]` y luego `doc.build(elements)`
