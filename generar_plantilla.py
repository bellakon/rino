#!/usr/bin/env python3
"""
Script para generar plantilla.pdf con reglas de incidencias y resumen de TecnoTime
"""
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime


def generar_plantilla_pdf():
    """Genera PDF con reglas de incidencias y resumen del sistema"""
    
    print("📄 Generando plantilla.pdf...")
    
    # Crear documento
    doc = SimpleDocTemplate(
        "plantilla.pdf",
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor('#1a5490'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=13,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor('#2c3e50')
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#34495e'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    # === PORTADA ===
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("TecnoTime", title_style))
    elements.append(Paragraph("Sistema de Gestión de Asistencias", subtitle_style))
    elements.append(Spacer(1, 30))
    
    # Información general
    elements.append(Paragraph("Descripción General del Sistema", section_style))
    
    info_general = [
        "<b>TecnoTime</b> es un sistema integral para la gestión y control de asistencias del personal. " +
        "Permite la integración con dispositivos checadores biométricos, procesamiento automático de " +
        "registros y generación de reportes detallados.",
        "",
        "<b>Módulos del Sistema:</b>",
        "",
        "<b>1. Checadores:</b> Administración de dispositivos biométricos ZKTeco. Permite configurar conexiones, " +
        "descargar registros de entrada/salida del personal y sincronizar datos automáticamente.",
        "",
        "<b>2. Asistencias:</b> Consulta y visualización de todas las checadas registradas. Incluye filtros por " +
        "trabajador, fecha y checador. Permite verificar los registros crudos antes de procesarlos.",
        "",
        "<b>3. Trabajadores:</b> Gestión completa del personal con información de número de empleado, nombre, " +
        "departamento, tipo de plaza y correo electrónico. Base fundamental para el control de asistencias.",
        "",
        "<b>4. Departamentos:</b> Organización del personal en áreas o departamentos. Facilita la segmentación " +
        "y generación de reportes por área.",
        "",
        "<b>5. Horarios:</b> Creación de plantillas de horarios con entrada/salida por día de la semana. " +
        "Permite asignar horarios específicos a trabajadores por periodo (semestre). Soporta horarios simples " +
        "(una entrada-salida) y mixtos (dos bloques de entrada-salida).",
        "",
        "<b>6. Bitácora:</b> Módulo principal que procesa las checadas contra los horarios asignados. " +
        "Calcula automáticamente retardos, salidas tempranas, faltas y horas trabajadas. Genera reportes " +
        "en PDF y permite envío por correo electrónico.",
        "",
        "<b>7. Movimientos:</b> Registro de incidencias especiales como permisos, incapacidades, comisiones, " +
        "licencias y otros movimientos que justifican ausencias o modifican el registro normal de asistencias.",
        "",
        f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    ]
    
    for texto in info_general:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 20))
    
    # === CÓDIGOS Y REGLAS DE INCIDENCIAS ===
    elements.append(PageBreak())
    elements.append(Paragraph("Códigos de Incidencias y Reglas de Cálculo", section_style))
    elements.append(Spacer(1, 10))
    
    intro_incidencias = [
        "El sistema calcula automáticamente las incidencias comparando las checadas registradas " +
        "contra el horario asignado a cada trabajador. A continuación se explican los códigos y reglas de cálculo:",
        "",
        "<b>Códigos de Incidencia (Columna 'Código' en bitácora):</b>",
        "• <b>A</b> = Asistencia normal",
        "• <b>R-</b> = Retardo Menor",
        "• <b>R+</b> = Retardo Mayor",
        "• <b>F</b> = Falta",
        "• <b>O</b> = Omisión (marcó entrada pero no salida, o viceversa)",
        "• <b>ST</b> = Salida Temprana",
        "• <b>J</b> = Justificado (con movimiento autorizado)",
        "• <b>L</b> = Licencia",
        "",
        "<b>Tipos de Falta (Columna 'Movimientos' en bitácora):</b>",
        "• <b>FNA</b> = Falta - No marcó asistencia (sin checadas de entrada)",
        "• <b>FRT</b> = Falta por retardo excesivo (más de 30 minutos tarde)",
        "• <b>FST</b> = Falta por salida muy tardía (más de 30 minutos después)",
        "• <b>FET</b> = Falta - Entrada demasiado temprana (antes de la ventana permitida)"
    ]
    
    for texto in intro_incidencias:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # === REGLAS DE ENTRADA ===
    elements.append(Paragraph("Reglas de Cálculo - ENTRADA", section_style))
    elements.append(Spacer(1, 5))
    
    reglas_entrada = [
        "<b>Ventana de entrada válida:</b>",
        "• Puede checar desde <b>30 minutos antes</b> de su hora de entrada",
        "• Ejemplo: Si su entrada es 08:00, puede checar desde 07:30",
        "• Si checa antes de 07:30 → Código: <b>F</b>, Movimiento: <b>FET</b>",
        "",
        "<b>Tolerancia de entrada (ASISTENCIA):</b>",
        "• Hasta <b>10 minutos tarde</b> → Código: <b>A</b>",
        "• Ejemplo: Horario 08:00, checa entre 07:30 y 08:10 → Asistencia normal",
        "",
        "<b>Retardo Menor (R-):</b>",
        "• De <b>11 a 16 minutos</b> de retardo → Código: <b>R-</b>",
        "• Ejemplo: Horario 08:00, checa entre 08:11 y 08:16",
        "",
        "<b>Retardo Mayor (R+):</b>",
        "• De <b>17 a 30 minutos</b> de retardo → Código: <b>R+</b>",
        "• Ejemplo: Horario 08:00, checa entre 08:17 y 08:30",
        "",
        "<b>Falta por retardo excesivo:</b>",
        "• <b>Más de 30 minutos</b> de retardo → Código: <b>F</b>, Movimiento: <b>FRT</b>",
        "• Ejemplo: Horario 08:00, checa a 08:31 o después → FALTA",
        "",
        "<b>Sin checada de entrada:</b>",
        "• No registró entrada → Código: <b>F</b>, Movimiento: <b>FNA</b>",
        "• Es el tipo de falta más grave"
    ]
    
    for texto in reglas_entrada:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # === REGLAS DE SALIDA NO DOCENTE ===
    elements.append(Paragraph("Reglas de Cálculo - SALIDA (Personal NO Docente)", section_style))
    elements.append(Spacer(1, 5))
    
    reglas_salida_no_docente = [
        "<b>Tolerancia de salida temprana:</b>",
        "• Puede salir hasta <b>25 minutos antes</b> sin problema → Código: <b>A</b>",
        "• Ejemplo: Horario salida 16:00, puede salir desde 15:35",
        "",
        "<b>Salida temprana (ST):</b>",
        "• Si sale <b>más de 25 minutos antes</b> → Código: <b>ST</b>",
        "• Ejemplo: Horario 16:00, sale a 15:30 → Salida Temprana",
        "",
        "<b>Salida tardía permitida:</b>",
        "• Hasta <b>30 minutos tarde</b> → Código: <b>A</b>",
        "• Ejemplo: Horario 16:00, checa hasta 16:30 → Asistencia normal",
        "",
        "<b>Falta por salida muy tardía:</b>",
        "• <b>Más de 30 minutos tarde</b> → Código: <b>F</b>, Movimiento: <b>FST</b>",
        "• Ejemplo: Horario 16:00, checa a 16:31 o después → FALTA",
        "",
        "<b>Sin checada de salida:</b>",
        "• Marcó entrada pero no salida → Código: <b>O</b> (Omisión)",
        "• El registro queda incompleto y debe revisarse"
    ]
    
    for texto in reglas_salida_no_docente:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # === REGLAS DE SALIDA DOCENTE ===
    elements.append(Paragraph("Reglas de Cálculo - SALIDA (Personal Docente)", section_style))
    elements.append(Spacer(1, 5))
    
    reglas_salida_docente = [
        "<b>Restricción especial:</b>",
        "• Los docentes <b>NO pueden salir antes</b> de su hora de salida",
        "• Deben checar EXACTAMENTE a su hora o después",
        "",
        "<b>Salida temprana (ST):</b>",
        "• Cualquier salida antes de su hora → Código: <b>ST</b>",
        "• Ejemplo: Horario 16:00, sale a 15:59 → Salida Temprana",
        "",
        "<b>Salida tardía permitida:</b>",
        "• Hasta <b>30 minutos tarde</b> → Código: <b>A</b>",
        "• Ejemplo: Horario 16:00, checa hasta 16:30 → Asistencia normal",
        "",
        "<b>Falta por salida muy tardía:</b>",
        "• <b>Más de 30 minutos tarde</b> → Código: <b>F</b>, Movimiento: <b>FST</b>",
        "• Ejemplo: Horario 16:00, checa a 16:31 o después → FALTA"
    ]
    
    for texto in reglas_salida_docente:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # === EJEMPLOS PRÁCTICOS ===
    elements.append(PageBreak())
    elements.append(Paragraph("Ejemplos Prácticos de Cálculo", section_style))
    elements.append(Spacer(1, 10))
    
    ejemplos = [
        "<b>Ejemplo 1: Asistencia normal</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: 08:05 (5 minutos tarde, dentro de tolerancia)",
        "• Checada 2: 16:10 (10 minutos tarde, dentro de tolerancia)",
        "• Resultado: Código <b>A</b> (Asistencia), Sin movimientos",
        "",
        "<b>Ejemplo 2: Retardo Menor</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: 08:14 (14 minutos tarde, retardo menor)",
        "• Checada 2: 16:05",
        "• Resultado: Código <b>R-</b> (Retardo Menor), Sin movimientos",
        "",
        "<b>Ejemplo 3: Retardo Mayor</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: 08:25 (25 minutos tarde, retardo mayor)",
        "• Checada 2: 16:00",
        "• Resultado: Código <b>R+</b> (Retardo Mayor), Sin movimientos",
        "",
        "<b>Ejemplo 4: Falta por retardo excesivo</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: 08:35 (35 minutos tarde, más de 30)",
        "• Checada 2: 16:00",
        "• Resultado: Código <b>F</b> (Falta), Movimiento <b>FRT</b>",
        "",
        "<b>Ejemplo 5: Falta sin checadas</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: No registró",
        "• Checada 2: No registró",
        "• Resultado: Código <b>F</b> (Falta), Movimiento <b>FNA</b>",
        "",
        "<b>Ejemplo 6: Omisión (no marcó salida)</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: 08:00",
        "• Checada 2: No registró",
        "• Resultado: Código <b>O</b> (Omisión), Sin movimientos",
        "",
        "<b>Ejemplo 7: Salida temprana (no docente)</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: 08:00",
        "• Checada 2: 15:30 (30 minutos antes, más de 25)",
        "• Resultado: Código <b>ST</b> (Salida Temprana), Sin movimientos",
        "",
        "<b>Ejemplo 8: Entrada demasiado temprana</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: 07:20 (40 minutos antes, más de 30)",
        "• Checada 2: 16:00",
        "• Resultado: Código <b>F</b> (Falta), Movimiento <b>FET</b>",
        "",
        "<b>Ejemplo 9: Con movimiento justificado</b>",
        "• Horario: 08:00 - 16:00",
        "• Checada 1: No registró",
        "• Checada 2: No registró",
        "• Movimiento: Permiso médico registrado",
        "• Resultado: Código <b>J</b> (Justificado), Movimiento: Nomenclatura del permiso"
    ]
    
    for texto in ejemplos:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # === NOTAS ADICIONALES ===
    elements.append(Paragraph("Notas Adicionales", section_style))
    elements.append(Spacer(1, 5))
    
    notas = [
        "<b>Detección de duplicados:</b>",
        "El sistema detecta y elimina checadas duplicadas automáticamente. Si dos checadas tienen menos de " +
        "60 segundos de diferencia, solo se registra la primera. Ejemplo: 09:16:00 y 09:16:56 se consideran " +
        "la misma checada.",
        "",
        "<b>Horarios mixtos:</b>",
        "Para horarios con dos bloques (ejemplo: 08:00-12:00, 14:00-16:00), el sistema valida cada bloque " +
        "por separado y considera los retardos de ambas entradas.",
        "",
        "<b>Movimientos especiales:</b>",
        "Los movimientos registrados en el sistema (permisos, incapacidades, comisiones, etc.) tienen prioridad " +
        "sobre el cálculo automático. Si existe un movimiento para el día, el código de incidencia cambia " +
        "según el tipo de movimiento.",
        "",
        "<b>Horas trabajadas:</b>",
        "El sistema calcula las horas trabajadas reales basándose en las checadas de entrada y salida, " +
        "independientemente del horario asignado.",
        "",
        "<b>Reporte semanal:</b>",
        "La bitácora muestra un resumen semanal con totales de asistencias, retardos, faltas y omisiones."
    ]
    
    for texto in notas:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    # === MANUAL DE USO - MÓDULOS ===
    elements.append(PageBreak())
    elements.append(Paragraph("Manual de Uso - Módulos del Sistema", section_style))
    elements.append(Spacer(1, 10))
    
    # MÓDULO CHECADORES
    elements.append(Paragraph("1. Módulo de Checadores", section_style))
    elements.append(Spacer(1, 5))
    
    modulo_checadores = [
        "<b>Descripción:</b>",
        "Administración de dispositivos biométricos ZKTeco conectados a la red. Permite descargar registros " +
        "de checadas automáticamente.",
        "",
        "<b>Configuración de dispositivos:</b>",
        "• Cada checador se configura con una IP fija en la red local",
        "• Serial: Identificador único del dispositivo (número de serie)",
        "• Ubicación: Nombre descriptivo (Entrada Principal, Recursos Humanos, etc.)",
        "• Puerto: Por defecto 4370 para dispositivos ZKTeco",
        "",
        "<b>Descargar registros:</b>",
        "1. Seleccionar uno o más checadores de la lista",
        "2. Hacer clic en 'Descargar Checadas'",
        "3. El sistema se conecta al dispositivo y descarga todos los registros nuevos",
        "4. Las checadas se guardan automáticamente en la base de datos",
        "",
        "<b>Probar conexión:</b>",
        "Use el botón 'Probar Conexión' para verificar que el dispositivo está accesible en la red. " +
        "Si falla, revise la IP, que el dispositivo esté encendido y conectado a la red.",
        "",
        "<b>Agregar nuevo checador:</b>",
        "1. Clic en 'Nuevo Checador'",
        "2. Ingresar Serial (número de serie del dispositivo)",
        "3. Ingresar IP (ejemplo: 192.168.1.100)",
        "4. Ingresar Ubicación descriptiva",
        "5. Puerto: Dejar 4370 (estándar ZKTeco)",
        "6. Guardar",
        "",
        "<b>Importar desde CSV:</b>",
        "Para agregar múltiples checadores, use la opción 'Importar CSV' con el formato:",
        "serial,ip,ubicacion,puerto"
    ]
    
    for texto in modulo_checadores:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # MÓDULO ASISTENCIAS
    elements.append(Paragraph("2. Módulo de Asistencias", section_style))
    elements.append(Spacer(1, 5))
    
    modulo_asistencias = [
        "<b>Descripción:</b>",
        "Consulta de registros crudos de checadas descargados de los dispositivos. Permite verificar " +
        "qué registros se han capturado antes de procesarlos en bitácora.",
        "",
        "<b>Filtros disponibles:</b>",
        "• Número de trabajador: Buscar por número específico",
        "• Nombre del trabajador: Búsqueda parcial por nombre",
        "• Checador (Serial): Filtrar por dispositivo específico",
        "• Rango de fechas: Desde - Hasta",
        "",
        "<b>Columnas mostradas:</b>",
        "• Número: Número de trabajador",
        "• Nombre: Nombre completo",
        "• Fecha: Día del registro",
        "• Hora: Hora exacta de la checada",
        "• Checador: Serial del dispositivo que registró",
        "",
        "<b>Ordenamiento:</b>",
        "Haga clic en los encabezados de las columnas para ordenar. Por defecto muestra los registros " +
        "más recientes primero.",
        "",
        "<b>Paginación:</b>",
        "El sistema muestra 50 registros por página para mejor rendimiento."
    ]
    
    for texto in modulo_asistencias:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # MÓDULO TRABAJADORES
    elements.append(PageBreak())
    elements.append(Paragraph("3. Módulo de Trabajadores", section_style))
    elements.append(Spacer(1, 5))
    
    modulo_trabajadores = [
        "<b>Descripción:</b>",
        "Gestión completa del personal. Base fundamental para el control de asistencias.",
        "",
        "<b>Información de cada trabajador:</b>",
        "• Número de trabajador: Identificador único (debe coincidir con ID en checador)",
        "• Nombre completo",
        "• Departamento: Área a la que pertenece",
        "• Tipo de plaza: DOCENTE, ADMINISTRATIVO, etc. (importante para reglas de asistencia)",
        "• Correo electrónico: Para envío de reportes de bitácora",
        "",
        "<b>Agregar trabajador:</b>",
        "1. Clic en 'Nuevo Trabajador'",
        "2. Ingresar número (debe ser único)",
        "3. Ingresar nombre completo",
        "4. Seleccionar departamento (debe existir previamente)",
        "5. Seleccionar tipo de plaza",
        "6. Ingresar correo electrónico (opcional pero recomendado)",
        "7. Guardar",
        "",
        "<b>IMPORTANTE - Tipo de plaza:</b>",
        "El tipo de plaza DOCENTE tiene reglas especiales de salida (no pueden salir antes de su hora). " +
        "El resto del personal tiene 25 minutos de tolerancia para salir antes.",
        "",
        "<b>Editar trabajador:</b>",
        "Haga clic en el ícono de editar (lápiz) en la fila del trabajador para modificar su información.",
        "",
        "<b>Eliminar trabajador:</b>",
        "Solo se puede eliminar si no tiene registros asociados (asistencias, horarios, movimientos). " +
        "Si tiene registros, considere marcarlo como inactivo en lugar de eliminarlo.",
        "",
        "<b>Importar desde CSV:</b>",
        "Para carga masiva, use 'Importar CSV' con el formato:",
        "num_trabajador,nombre,departamento,tipo_plaza,correo",
        "El departamento debe existir previamente en el sistema."
    ]
    
    for texto in modulo_trabajadores:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # MÓDULO DEPARTAMENTOS
    elements.append(Paragraph("4. Módulo de Departamentos", section_style))
    elements.append(Spacer(1, 5))
    
    modulo_departamentos = [
        "<b>Descripción:</b>",
        "Organización del personal en áreas o departamentos. Facilita la segmentación de reportes.",
        "",
        "<b>Agregar departamento:</b>",
        "1. Clic en 'Nuevo Departamento'",
        "2. Ingresar nombre del departamento",
        "3. Ingresar descripción (opcional)",
        "4. Guardar",
        "",
        "<b>Uso:</b>",
        "Los departamentos se utilizan al registrar trabajadores y permiten filtrar reportes por área. " +
        "Cree los departamentos antes de agregar trabajadores.",
        "",
        "<b>Importar desde CSV:</b>",
        "Formato: nombre,descripcion"
    ]
    
    for texto in modulo_departamentos:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # MÓDULO HORARIOS
    elements.append(PageBreak())
    elements.append(Paragraph("5. Módulo de Horarios", section_style))
    elements.append(Spacer(1, 5))
    
    modulo_horarios = [
        "<b>Descripción:</b>",
        "Creación de plantillas de horarios y asignación a trabajadores por periodo (semestre).",
        "",
        "<b>Estructura de dos tabs:</b>",
        "• <b>Plantillas de Horarios:</b> Define los horarios base (entrada/salida por día)",
        "• <b>Asignaciones:</b> Asigna plantillas a trabajadores con fechas de vigencia",
        "",
        "<b>--- TAB 1: Plantillas de Horarios ---</b>",
        "",
        "<b>Crear plantilla:</b>",
        "1. Clic en 'Nueva Plantilla'",
        "2. Ingresar nombre descriptivo (ejemplo: 'Horario Administrativo Matutino')",
        "3. Definir horario para cada día de la semana:",
        "   • Formato simple: 08:00-16:00 (una entrada, una salida)",
        "   • Formato mixto: 08:00-12:00,14:00-16:00 (dos bloques con comida)",
        "   • Descanso: 00:00-00:00",
        "4. Guardar",
        "",
        "<b>Tipos de horario:</b>",
        "• <b>Simple:</b> Una entrada y una salida (08:00-16:00)",
        "• <b>Mixto:</b> Dos bloques separados por coma (08:00-12:00,14:00-16:00)",
        "• <b>Descanso:</b> Usar 00:00-00:00 para días sin trabajo",
        "",
        "<b>Ejemplos de plantillas:</b>",
        "• Turno matutino: Lun-Vie 07:00-15:00, Sáb-Dom 00:00-00:00",
        "• Turno vespertino: Lun-Vie 15:00-23:00, Sáb-Dom 00:00-00:00",
        "• Administrativo: Lun-Vie 08:00-16:00, Sáb-Dom 00:00-00:00",
        "• Con comida: Lun-Vie 08:00-14:00,16:00-18:00, Sáb-Dom 00:00-00:00",
        "",
        "<b>--- TAB 2: Asignaciones ---</b>",
        "",
        "<b>Asignar horario a trabajador:</b>",
        "1. Clic en 'Nueva Asignación'",
        "2. Seleccionar trabajador",
        "3. Seleccionar plantilla de horario",
        "4. Ingresar fecha inicio (ejemplo: 01/08/2024)",
        "5. Ingresar fecha fin (ejemplo: 31/12/2024)",
        "6. Seleccionar semestre (Enero-Junio o Agosto-Diciembre)",
        "7. Guardar",
        "",
        "<b>IMPORTANTE - Vigencia:</b>",
        "Las asignaciones tienen fecha de inicio y fin. El sistema usa estas fechas para determinar qué " +
        "horario aplicar al procesar la bitácora. Un trabajador puede tener diferentes horarios en " +
        "diferentes periodos.",
        "",
        "<b>Validación de traslapes:</b>",
        "El sistema detecta si ya existe una asignación para el trabajador en el mismo periodo y no permite " +
        "traslapes. Para cambiar de horario, la asignación anterior debe terminar antes de que inicie la nueva.",
        "",
        "<b>Filtros en asignaciones:</b>",
        "• Número de trabajador",
        "• Nombre de trabajador",
        "• Semestre",
        "• Estado (Vigente/Vencida/Futura)",
        "",
        "<b>Importar asignaciones desde CSV:</b>",
        "Formato: num_trabajador,nombre_plantilla,fecha_inicio,fecha_fin,semestre",
        "Las fechas deben estar en formato DD/MM/YYYY o DD/MM/YY"
    ]
    
    for texto in modulo_horarios:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # MÓDULO BITÁCORA
    elements.append(PageBreak())
    elements.append(Paragraph("6. Módulo de Bitácora", section_style))
    elements.append(Spacer(1, 5))
    
    modulo_bitacora = [
        "<b>Descripción:</b>",
        "Módulo principal que procesa las checadas contra los horarios asignados. Genera reportes " +
        "detallados en PDF y permite envío por correo electrónico.",
        "",
        "<b>Procesar bitácora individual:</b>",
        "1. Seleccionar 'Individual' en el tipo de proceso",
        "2. Seleccionar trabajador del dropdown",
        "3. Seleccionar rango de fechas (ejemplo: semana o quincena)",
        "4. Clic en 'Procesar Bitácora'",
        "5. El sistema compara las checadas con el horario asignado",
        "6. Muestra tabla con código de incidencia por cada día",
        "",
        "<b>Procesar bitácora masiva (múltiples trabajadores):</b>",
        "1. Seleccionar 'Masivo' en el tipo de proceso",
        "2. Seleccionar departamento (opcional, para filtrar)",
        "3. Seleccionar rango de fechas",
        "4. Clic en 'Procesar Masivo'",
        "5. El sistema procesa todos los trabajadores del departamento",
        "",
        "<b>Información mostrada en la bitácora:</b>",
        "• Fecha y día de la semana",
        "• Horario asignado (entrada-salida esperada)",
        "• Checada 1 (entrada registrada)",
        "• Checada 2 (salida registrada)",
        "• Checada 3 y 4 (para horarios mixtos)",
        "• Código: A, R-, R+, F, O, ST (ver sección de códigos)",
        "• Movimientos: FNA, FRT, FST o movimiento registrado",
        "• Retardo: Minutos de retardo en entrada",
        "• Horas trabajadas: Tiempo real trabajado",
        "",
        "<b>Resumen semanal:</b>",
        "Al final de cada semana se muestra un resumen con:",
        "• Total de asistencias (A)",
        "• Total de retardos menores (R-)",
        "• Total de retardos mayores (R+)",
        "• Total de faltas (F)",
        "• Total de omisiones (O)",
        "• Total de salidas tempranas (ST)",
        "",
        "<b>Descargar PDF:</b>",
        "1. Después de procesar, clic en 'Descargar PDF'",
        "2. Se genera un PDF con el formato oficial de bitácora",
        "3. Incluye encabezado institucional",
        "4. Tabla completa de asistencias",
        "5. Resumen semanal",
        "",
        "<b>Enviar por correo:</b>",
        "1. Después de procesar, clic en 'Enviar por Correo'",
        "2. El sistema verifica que el trabajador tenga correo registrado",
        "3. Genera el PDF automáticamente",
        "4. Envía correo con el PDF adjunto",
        "5. También adjunta el archivo plantilla.pdf (este manual)",
        "",
        "<b>Configuración de correo:</b>",
        "Debe configurarse previamente en el archivo .env:",
        "• SMTP_HOST: Servidor de correo (smtp.office365.com para Outlook)",
        "• SMTP_PORT: 587",
        "• SMTP_USER: Correo del remitente",
        "• SMTP_PASSWORD: Contraseña de aplicación (no la contraseña normal)",
        "",
        "<b>NOTA IMPORTANTE:</b>",
        "Para Outlook/Office365 debe generar una contraseña de aplicación en:",
        "https://account.microsoft.com → Seguridad → Contraseñas de aplicación"
    ]
    
    for texto in modulo_bitacora:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # MÓDULO MOVIMIENTOS
    elements.append(PageBreak())
    elements.append(Paragraph("7. Módulo de Movimientos", section_style))
    elements.append(Spacer(1, 5))
    
    modulo_movimientos = [
        "<b>Descripción:</b>",
        "Registro de incidencias especiales que justifican ausencias o modifican el registro automático " +
        "de asistencias.",
        "",
        "<b>Estructura de dos tabs:</b>",
        "• <b>Tipos de Movimientos:</b> Catálogo de códigos (permisos, licencias, etc.)",
        "• <b>Movimientos Realizados:</b> Registro de incidencias aplicadas a trabajadores",
        "",
        "<b>--- TAB 1: Tipos de Movimientos ---</b>",
        "",
        "<b>Campos de un tipo:</b>",
        "• Nomenclatura: Código único (ejemplo: COM001, PER001)",
        "• Nombre: Descripción corta (Comisión oficial, Permiso médico)",
        "• Categoría: Comisión, Permiso, Incapacidad, Licencia, Otros",
        "• Letra: Símbolo que aparece en bitácora (J, L, A)",
        "• Descripción: Detalle completo",
        "",
        "<b>Letras comunes:</b>",
        "• J = Justificado (permisos, comisiones)",
        "• L = Licencia (maternidad, paternidad, etc.)",
        "• A = Autorizado (actividades especiales)",
        "",
        "<b>--- TAB 2: Movimientos Realizados ---</b>",
        "",
        "<b>Registrar movimiento individual:</b>",
        "1. Clic en 'Nuevo Movimiento'",
        "2. Seleccionar trabajador",
        "3. Seleccionar tipo de movimiento",
        "4. Seleccionar fecha del movimiento",
        "5. Agregar observaciones (opcional)",
        "6. Si el tipo tiene campos personalizados, llenarlos",
        "7. Guardar",
        "",
        "<b>Asignación masiva:</b>",
        "Para aplicar el mismo movimiento a varios trabajadores:",
        "1. Clic en 'Asignación Masiva'",
        "2. Seleccionar tipo de movimiento",
        "3. Seleccionar fecha",
        "4. Seleccionar múltiples trabajadores (mantener Ctrl/Cmd)",
        "5. Agregar observaciones",
        "6. Guardar",
        "",
        "<b>Efecto en bitácora:</b>",
        "Cuando se procesa la bitácora, si existe un movimiento para ese día:",
        "• El código de incidencia cambia según la letra del tipo",
        "• La nomenclatura aparece en la columna 'Movimientos'",
        "• Las checadas se siguen mostrando pero no afectan el código",
        "",
        "<b>Importar desde CSV:</b>",
        "Formato: num_trabajador,tipo_movimiento,fecha,observaciones",
        "El tipo_movimiento debe ser la nomenclatura exacta",
        "",
        "<b>Ejemplo práctico:</b>",
        "Trabajador tiene permiso médico el 15/11/2024:",
        "1. Crear movimiento: Trabajador 100, Tipo: PER-MED, Fecha: 15/11/2024",
        "2. Al procesar bitácora del 15/11, aunque no tenga checadas:",
        "   • Código: J (Justificado)",
        "   • Movimientos: PER-MED",
        "   • No cuenta como falta"
    ]
    
    for texto in modulo_movimientos:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    elements.append(Spacer(1, 15))
    
    # RECOMENDACIONES Y FLUJO
    elements.append(PageBreak())
    elements.append(Paragraph("Flujo de Trabajo Recomendado", section_style))
    elements.append(Spacer(1, 5))
    
    flujo = [
        "<b>Configuración inicial (una vez):</b>",
        "1. Configurar checadores (IPs y ubicaciones)",
        "2. Crear departamentos",
        "3. Registrar trabajadores",
        "4. Crear plantillas de horarios",
        "5. Asignar horarios a trabajadores",
        "6. Crear tipos de movimientos comunes",
        "",
        "<b>Operación diaria/semanal:</b>",
        "1. Descargar checadas de los dispositivos (diario o según necesidad)",
        "2. Registrar movimientos especiales (permisos, incapacidades)",
        "3. Procesar bitácora (semanal, quincenal o mensual)",
        "4. Revisar incidencias y corregir si es necesario",
        "5. Generar y enviar reportes",
        "",
        "<b>Casos especiales:</b>",
        "• Si un trabajador olvidó checar: Registrar movimiento de omisión",
        "• Si cambió de horario: Crear nueva asignación con fechas correctas",
        "• Si hubo falla en checador: Descargar de nuevo o registrar manualmente",
        "• Si hay error en bitácora: Verificar horario asignado y checadas originales",
        "",
        "<b>Mantenimiento:</b>",
        "• Actualizar asignaciones de horarios cada semestre",
        "• Verificar correos de trabajadores estén actualizados",
        "• Revisar conexión de checadores periódicamente",
        "• Respaldar base de datos regularmente"
    ]
    
    for texto in flujo:
        if texto:
            elements.append(Paragraph(texto, body_style))
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    elements.append(Paragraph(
        f"TecnoTime - Sistema de Gestión de Asistencias | " +
        f"Generado: {datetime.now().strftime('%d/%m/%Y')}",
        footer_style
    ))
    
    # Construir PDF
    print("📝 Generando archivo PDF...")
    doc.build(elements)
    
    print("✅ Archivo plantilla.pdf generado exitosamente")
    return True


if __name__ == '__main__':
    try:
        exito = generar_plantilla_pdf()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
