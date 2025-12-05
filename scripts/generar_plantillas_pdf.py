"""
Script para generar los PDFs de documentación del sistema TecnoTime
- plantilla.pdf: Documentación completa del sistema para administradores
- plantilla_trabajadores.pdf: Guía simple para trabajadores
"""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime


def crear_estilos():
    """Crea los estilos personalizados para los PDFs"""
    styles = getSampleStyleSheet()
    
    # Título principal
    styles.add(ParagraphStyle(
        name='TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=12,
        textColor=HexColor('#1a5276'),
        alignment=1  # Centrado
    ))
    
    # Subtítulo
    styles.add(ParagraphStyle(
        name='Subtitulo',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=HexColor('#2874a6')
    ))
    
    # Sección
    styles.add(ParagraphStyle(
        name='Seccion',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=HexColor('#1a5276')
    ))
    
    # Texto normal con espaciado
    styles.add(ParagraphStyle(
        name='TextoNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,
        spaceAfter=4,
        leading=14
    ))
    
    # Texto destacado
    styles.add(ParagraphStyle(
        name='TextoDestacado',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,
        spaceAfter=4,
        leading=14,
        backColor=HexColor('#fef9e7'),
        borderPadding=5
    ))
    
    # Nota/Referencia
    styles.add(ParagraphStyle(
        name='Referencia',
        parent=styles['Normal'],
        fontSize=9,
        spaceBefore=2,
        spaceAfter=2,
        textColor=HexColor('#566573'),
        leftIndent=20
    ))
    
    # Pie de página
    styles.add(ParagraphStyle(
        name='PiePagina',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor('#7f8c8d'),
        alignment=1
    ))
    
    return styles


def crear_tabla(data, col_widths=None, header_color='#2874a6'):
    """Crea una tabla con estilo consistente"""
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(header_color)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#bdc3c7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f8f9f9')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return table


def generar_plantilla_trabajadores():
    """
    Genera plantilla_trabajadores.pdf
    Guía compacta para que los trabajadores entiendan sus incidencias
    """
    doc = SimpleDocTemplate(
        "plantilla_trabajadores.pdf",
        pagesize=LETTER,
        rightMargin=0.6*inch,
        leftMargin=0.6*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    styles = crear_estilos()
    story = []
    
    # ==========================================
    # ENCABEZADO
    # ==========================================
    story.append(Paragraph("TecnoTime - Guía de Asistencias", styles['TituloPrincipal']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "Esta guía explica los códigos que aparecen en tu bitácora de asistencias y las reglas "
        "que el sistema aplica para calcularlos.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # ==========================================
    # CÓDIGOS DE INCIDENCIA
    # ==========================================
    story.append(Paragraph("Códigos de Incidencia", styles['Subtitulo']))
    
    codigos_data = [
        ['Código', 'Significado', 'Descripción'],
        ['A', 'Asistencia', 'Checaste correctamente dentro de tu horario.'],
        ['R-', 'Retardo Menor', 'Llegaste entre 11 y 20 minutos tarde.'],
        ['R+', 'Retardo Mayor', 'Llegaste entre 21 y 30 minutos tarde.'],
        ['F', 'Falta', 'No checaste o llegaste más de 30 minutos tarde.'],
        ['O', 'Omisión', 'Falta tu checada de entrada o salida.'],
        ['ST', 'Salida Temprana', 'Saliste antes de tu hora asignada.'],
        ['J', 'Justificado', 'Tienes permiso o justificante autorizado.'],
        ['L', 'Licencia', 'Licencia oficial registrada.'],
    ]
    
    story.append(crear_tabla(codigos_data, col_widths=[0.6*inch, 1.2*inch, 4.5*inch]))
    story.append(Spacer(1, 0.15*inch))
    
    # Tipos de Falta
    story.append(Paragraph("Cuando aparece Falta (F), el sistema indica el motivo:", styles['TextoNormal']))
    
    faltas_data = [
        ['Tipo', 'Significado'],
        ['NA', 'No marcó Asistencia - No registraste checada de entrada.'],
        ['FH', 'Fuera de Horario - Checaste muy temprano o muy tarde.'],
    ]
    
    story.append(crear_tabla(faltas_data, col_widths=[0.6*inch, 5.7*inch]))
    story.append(Spacer(1, 0.25*inch))
    
    # ==========================================
    # REGLAS DE ENTRADA Y SALIDA
    # ==========================================
    story.append(Paragraph("Reglas de Entrada", styles['Subtitulo']))
    
    entrada_data = [
        ['Situación', 'Código'],
        ['Más de 20 min antes de tu hora', 'F (Fuera de Horario)'],
        ['Desde 20 min antes hasta 10 min tarde', 'A (Asistencia)'],
        ['De 11 a 20 minutos tarde', 'R- (Retardo Menor)'],
        ['De 21 a 30 minutos tarde', 'R+ (Retardo Mayor)'],
        ['Más de 30 minutos tarde', 'F (Falta)'],
    ]
    
    story.append(crear_tabla(entrada_data, col_widths=[3.5*inch, 2.8*inch]))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Reglas de Salida", styles['Subtitulo']))
    
    # Tabla comparativa compacta
    salida_data = [
        ['Situación', 'No Docente', 'Docente'],
        ['Salida anticipada', '> 5 min antes = ST', 'Cualquier min antes = ST'],
        ['Salida normal', 'Hasta 20 min después = A', 'Hasta 20 min después = A'],
        ['Salida muy tarde', '> 20 min después = F (FH)', '> 20 min después = F (FH)'],
    ]
    
    story.append(crear_tabla(salida_data, col_widths=[1.8*inch, 2.2*inch, 2.3*inch]))
    story.append(Spacer(1, 0.2*inch))
    
    # ==========================================
    # EJEMPLO RÁPIDO
    # ==========================================
    story.append(Paragraph("Ejemplo: Horario 8:00 - 16:00", styles['Seccion']))
    
    ejemplo_data = [
        ['Checaste entrada', 'Resultado'],
        ['7:35 o antes', 'F (FH) - Muy temprano'],
        ['7:40 a 8:10', 'A - Correcto'],
        ['8:15', 'R- (15 min tarde)'],
        ['8:25', 'R+ (25 min tarde)'],
        ['8:35 o después', 'F - Falta'],
    ]
    
    story.append(crear_tabla(ejemplo_data, col_widths=[2*inch, 4.3*inch], header_color='#27ae60'))
    story.append(Spacer(1, 0.25*inch))
    
    # ==========================================
    # PREGUNTAS FRECUENTES (compacto)
    # ==========================================
    story.append(Paragraph("Preguntas Frecuentes", styles['Subtitulo']))
    
    story.append(Paragraph(
        "<b>¿Por qué Omisión si trabajé?</b> Checaste entrada pero no salida. Asegúrate de checar al retirarte.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>¿Cómo justifico una falta?</b> Solicita permiso a tu jefe de departamento. Se registrará como J (Justificado).",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>¿Falta por llegar temprano?</b> Checar más de 20 min antes se considera Fuera de Horario (FH).",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.25*inch))
    
    # ==========================================
    # FUNDAMENTO (compacto)
    # ==========================================
    story.append(Paragraph("Fundamento Reglamentario", styles['Subtitulo']))
    
    story.append(Paragraph(
        "Las reglas están basadas en los reglamentos oficiales del TECNM:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "<b>Art. 80 (SEP) y Art. 153 (TECNM):</b> Tolerancia de 10 min. Retardo menor: 11-20 min. "
        "Retardo mayor: 21-30 min. Más de 30 min = Falta.",
        styles['Referencia']
    ))
    story.append(Paragraph(
        "<b>Art. 103 (No Docentes):</b> Ventana válida de 20 min antes de entrada y 20 min después de salida.",
        styles['Referencia']
    ))
    story.append(Paragraph(
        "<b>Art. 98-100:</b> Se considera falta cuando no se presenta, llega después de 30 min, "
        "o no registra entrada/salida.",
        styles['Referencia']
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    fecha_gen = datetime.now().strftime("%d/%m/%Y")
    story.append(Paragraph(
        f"TecnoTime - Guía de Asistencias | {fecha_gen}",
        styles['PiePagina']
    ))
    
    # Generar PDF
    doc.build(story)
    print("✅ Generado: plantilla_trabajadores.pdf (1 página)")


def generar_plantilla_sistema():
    """
    Genera plantilla.pdf
    Documentación completa del sistema para administradores
    """
    doc = SimpleDocTemplate(
        "plantilla.pdf",
        pagesize=LETTER,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = crear_estilos()
    story = []
    
    # ==========================================
    # PORTADA
    # ==========================================
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("TecnoTime", styles['TituloPrincipal']))
    story.append(Paragraph("Sistema de Gestión de Asistencias", styles['Subtitulo']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Manual de Administración", styles['Seccion']))
    story.append(Spacer(1, 1*inch))
    
    story.append(Paragraph(
        "Este documento describe el funcionamiento del sistema TecnoTime, incluyendo "
        "los módulos disponibles, las reglas de cálculo de incidencias y los procedimientos "
        "recomendados para la administración de asistencias.",
        styles['TextoNormal']
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # DESCRIPCIÓN GENERAL
    # ==========================================
    story.append(Paragraph("Descripción General", styles['Subtitulo']))
    
    story.append(Paragraph(
        "TecnoTime es un sistema integral para la gestión y control de asistencias del personal. "
        "Permite la integración con dispositivos checadores biométricos ZKTeco, procesamiento "
        "automático de registros y generación de reportes detallados.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Módulos del Sistema:", styles['Seccion']))
    
    modulos = [
        ("1. Checadores", "Administración de dispositivos biométricos. Permite configurar conexiones, "
         "descargar registros de entrada/salida y sincronizar datos."),
        ("2. Asistencias", "Consulta de registros crudos de checadas. Permite verificar los datos "
         "antes de procesarlos en bitácora."),
        ("3. Trabajadores", "Gestión del personal con información de número, nombre, departamento, "
         "tipo de plaza y correo electrónico."),
        ("4. Departamentos", "Organización del personal en áreas. Facilita la segmentación de reportes."),
        ("5. Horarios", "Creación de plantillas de horarios y asignación a trabajadores por periodo."),
        ("6. Bitácora", "Módulo principal que procesa checadas contra horarios. Calcula incidencias "
         "automáticamente y genera reportes PDF."),
        ("7. Movimientos", "Registro de permisos, incapacidades, comisiones y justificantes."),
    ]
    
    for titulo, desc in modulos:
        story.append(Paragraph(f"<b>{titulo}:</b> {desc}", styles['TextoNormal']))
    
    story.append(PageBreak())
    
    # ==========================================
    # CÓDIGOS DE INCIDENCIA
    # ==========================================
    story.append(Paragraph("Códigos de Incidencias", styles['Subtitulo']))
    
    story.append(Paragraph(
        "El sistema calcula automáticamente las incidencias comparando las checadas registradas "
        "contra el horario asignado a cada trabajador. Los códigos se muestran en la columna "
        "'Código' de la bitácora:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    codigos_data = [
        ['Código', 'Nombre', 'Descripción'],
        ['A', 'Asistencia', 'Checó correctamente dentro del horario permitido'],
        ['R-', 'Retardo Menor', 'Llegó entre 11 y 20 minutos tarde'],
        ['R+', 'Retardo Mayor', 'Llegó entre 21 y 30 minutos tarde'],
        ['F', 'Falta', 'No checó entrada o llegó más de 30 minutos tarde'],
        ['O', 'Omisión', 'Checó entrada pero no salida (o viceversa)'],
        ['ST', 'Salida Temprana', 'Salió antes de la hora permitida'],
        ['J', 'Justificado', 'Tiene movimiento autorizado (permiso, comisión)'],
        ['L', 'Licencia', 'Tiene licencia oficial registrada'],
    ]
    
    story.append(crear_tabla(codigos_data, col_widths=[0.7*inch, 1.3*inch, 4.3*inch]))
    story.append(Spacer(1, 0.3*inch))
    
    # Tipos de Falta
    story.append(Paragraph("Tipos de Falta (columna 'Movimientos'):", styles['Seccion']))
    
    story.append(Paragraph(
        "Cuando el código es F (Falta), el sistema especifica el tipo en la columna de movimientos:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    faltas_data = [
        ['Tipo', 'Nombre', 'Descripción'],
        ['NA', 'No marcó Asistencia', 'No registró checada de entrada ese día'],
        ['FH', 'Fuera de Horario', 'Checó fuera de la ventana permitida (muy temprano o muy tarde)'],
    ]
    
    story.append(crear_tabla(faltas_data, col_widths=[0.7*inch, 1.8*inch, 3.8*inch]))
    
    story.append(PageBreak())
    
    # ==========================================
    # REGLAS DE CÁLCULO - ENTRADA
    # ==========================================
    story.append(Paragraph("Reglas de Cálculo - Entrada", styles['Subtitulo']))
    
    story.append(Paragraph(
        "El sistema aplica las siguientes reglas para evaluar la checada de entrada. "
        "Estas reglas están basadas en los reglamentos oficiales del TECNM:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    entrada_data = [
        ['Condición', 'Código', 'Movimiento', 'Base Reglamentaria'],
        ['Más de 20 min antes de la hora', 'F', 'FH', 'Art. 103 Reg. No Docentes'],
        ['Desde 20 min antes hasta la hora', 'A', '-', 'Ventana válida de entrada'],
        ['De 1 a 10 minutos tarde', 'A', '-', 'Tolerancia Art. 80, 153'],
        ['De 11 a 20 minutos tarde', 'R-', '-', 'Art. 80a SEP, Art. 153a TECNM'],
        ['De 21 a 30 minutos tarde', 'R+', '-', 'Art. 80b SEP, Art. 153b TECNM'],
        ['Más de 30 minutos tarde', 'F', 'FH', 'Art. 98, 99 Reg. Interior'],
        ['Sin checada de entrada', 'F', 'NA', 'Art. 100 Reg. Interior'],
    ]
    
    story.append(crear_tabla(entrada_data, col_widths=[2.2*inch, 0.7*inch, 0.9*inch, 2.5*inch]))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "<b>Nota:</b> La ventana de 20 minutos antes aplica específicamente al personal no docente "
        "según el Art. 103 del Reglamento Interno de Trabajo para Personal No Docente.",
        styles['Referencia']
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # REGLAS DE CÁLCULO - SALIDA
    # ==========================================
    story.append(Paragraph("Reglas de Cálculo - Salida", styles['Subtitulo']))
    
    story.append(Paragraph(
        "Las reglas de salida difieren entre personal docente y no docente, según lo establecido "
        "en sus respectivos reglamentos:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Personal No Docente
    story.append(Paragraph("Personal No Docente (Administrativo):", styles['Seccion']))
    
    salida_no_docente = [
        ['Condición', 'Código', 'Movimiento', 'Base'],
        ['Más de 5 minutos antes de la hora', 'ST', '-', 'Salida anticipada sin autorización'],
        ['Hasta 5 min antes o después de la hora', 'A', '-', 'Tolerancia de salida'],
        ['Hasta 20 minutos después de la hora', 'A', '-', 'Art. 103b Reg. No Docentes'],
        ['Más de 20 minutos después', 'F', 'FH', 'Art. 103b Reg. No Docentes'],
        ['Sin checada de salida', 'O', '-', 'Omisión de registro'],
    ]
    
    story.append(crear_tabla(salida_no_docente, col_widths=[2.5*inch, 0.7*inch, 0.9*inch, 2.2*inch]))
    story.append(Spacer(1, 0.2*inch))
    
    # Personal Docente
    story.append(Paragraph("Personal Docente:", styles['Seccion']))
    
    story.append(Paragraph(
        "Los docentes tienen restricciones más estrictas para la salida, ya que deben cumplir "
        "el tiempo completo de sus horas clase:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    salida_docente = [
        ['Condición', 'Código', 'Movimiento', 'Base'],
        ['Cualquier minuto antes de la hora', 'ST', '-', 'Art. 153 - Sin tolerancia'],
        ['A la hora exacta o después', 'A', '-', 'Cumplimiento del horario'],
        ['Hasta 20 minutos después de la hora', 'A', '-', 'Ventana válida de salida'],
        ['Más de 20 minutos después', 'F', 'FH', 'Fuera de horario'],
        ['Sin checada de salida', 'O', '-', 'Omisión de registro'],
    ]
    
    story.append(crear_tabla(salida_docente, col_widths=[2.5*inch, 0.7*inch, 0.9*inch, 2.2*inch]))
    
    story.append(PageBreak())
    
    # ==========================================
    # RESUMEN COMPARATIVO
    # ==========================================
    story.append(Paragraph("Resumen Comparativo: Docentes vs No Docentes", styles['Subtitulo']))
    
    comparativo = [
        ['Concepto', 'No Docentes', 'Docentes'],
        ['Ventana entrada temprana', '20 min antes (Art. 103a)', '20 min antes'],
        ['Tolerancia de entrada', '10 minutos', '10 minutos'],
        ['Retardo Menor', '11-20 min tarde', '11-20 min tarde'],
        ['Retardo Mayor', '21-30 min tarde', '21-30 min tarde'],
        ['Falta por retardo', '+30 min tarde', '+30 min tarde'],
        ['Tolerancia salida temprana', '5 minutos', '0 minutos'],
        ['Ventana salida tardía', '20 min después (Art. 103b)', '20 min después'],
    ]
    
    table = crear_tabla(comparativo, col_widths=[2.5*inch, 2*inch, 1.8*inch])
    story.append(table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "<b>Diferencia clave:</b> Los docentes NO tienen tolerancia de salida temprana. "
        "Cualquier salida antes de su hora asignada se registra como ST (Salida Temprana). "
        "El personal no docente tiene 5 minutos de tolerancia.",
        styles['TextoDestacado']
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # EJEMPLOS PRÁCTICOS
    # ==========================================
    story.append(Paragraph("Ejemplos Prácticos", styles['Subtitulo']))
    
    ejemplos = [
        ("Ejemplo 1: Asistencia normal",
         "Horario: 08:00-16:00 | Entrada: 08:05 | Salida: 16:10",
         "Código: A | Movimiento: - | El trabajador llegó dentro de tolerancia."),
        
        ("Ejemplo 2: Retardo Menor",
         "Horario: 08:00-16:00 | Entrada: 08:15 | Salida: 16:00",
         "Código: R- | Movimiento: - | 15 minutos de retardo (rango 11-20)."),
        
        ("Ejemplo 3: Retardo Mayor",
         "Horario: 08:00-16:00 | Entrada: 08:25 | Salida: 16:00",
         "Código: R+ | Movimiento: - | 25 minutos de retardo (rango 21-30)."),
        
        ("Ejemplo 4: Falta por retardo excesivo",
         "Horario: 08:00-16:00 | Entrada: 08:35 | Salida: 16:00",
         "Código: F | Movimiento: FH | Más de 30 minutos tarde = Fuera de Horario."),
        
        ("Ejemplo 5: Sin checadas",
         "Horario: 08:00-16:00 | Entrada: No registró | Salida: No registró",
         "Código: F | Movimiento: NA | No marcó asistencia."),
        
        ("Ejemplo 6: Omisión",
         "Horario: 08:00-16:00 | Entrada: 08:00 | Salida: No registró",
         "Código: O | Movimiento: - | Checó entrada pero no salida."),
        
        ("Ejemplo 7: Entrada muy temprana",
         "Horario: 08:00-16:00 | Entrada: 07:30 | Salida: 16:00",
         "Código: F | Movimiento: FH | Checó 30 min antes (límite 20 min)."),
        
        ("Ejemplo 8: Salida temprana (no docente)",
         "Horario: 08:00-16:00 | Entrada: 08:00 | Salida: 15:50",
         "Código: ST | Movimiento: - | Salió 10 min antes (tolerancia es 5 min)."),
        
        ("Ejemplo 9: Con movimiento justificado",
         "Horario: 08:00-16:00 | Sin checadas | Tiene permiso médico registrado",
         "Código: J | Movimiento: PER-MED | El permiso tiene prioridad."),
    ]
    
    for titulo, situacion, resultado in ejemplos:
        story.append(Paragraph(f"<b>{titulo}</b>", styles['TextoNormal']))
        story.append(Paragraph(situacion, styles['Referencia']))
        story.append(Paragraph(resultado, styles['TextoNormal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # ==========================================
    # MÓDULOS DEL SISTEMA
    # ==========================================
    story.append(Paragraph("Guía de Módulos", styles['Subtitulo']))
    
    # Checadores
    story.append(Paragraph("1. Módulo de Checadores", styles['Seccion']))
    story.append(Paragraph(
        "Administra los dispositivos biométricos ZKTeco conectados a la red. Permite descargar "
        "automáticamente los registros de entrada y salida del personal.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Configuración de dispositivos:</b><br/>"
        "• <b>Serial:</b> Número de serie único del dispositivo (aparece en la etiqueta del equipo)<br/>"
        "• <b>IP:</b> Dirección en la red local (ej: 192.168.1.100)<br/>"
        "• <b>Puerto:</b> Por defecto 4370 para ZKTeco<br/>"
        "• <b>Ubicación:</b> Nombre descriptivo (Entrada Principal, Recursos Humanos, etc.)",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Operaciones disponibles:</b><br/>"
        "• <b>Descargar checadas:</b> Selecciona uno o más dispositivos y haz clic en 'Descargar'. "
        "El sistema se conecta, descarga todos los registros nuevos y los guarda en la base de datos.<br/>"
        "• <b>Probar conexión:</b> Verifica que el dispositivo esté accesible. Si falla, revisa la IP "
        "y que el equipo esté encendido y conectado a la red.<br/>"
        "• <b>Importar CSV:</b> Para agregar múltiples checadores. Formato: serial,ip,ubicacion,puerto",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Asistencias
    story.append(Paragraph("2. Módulo de Asistencias", styles['Seccion']))
    story.append(Paragraph(
        "Consulta los registros crudos de checadas descargados de los dispositivos. Permite verificar "
        "qué registros se han capturado antes de procesarlos en la bitácora.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Filtros disponibles:</b><br/>"
        "• Número de trabajador: Buscar por número específico<br/>"
        "• Nombre: Búsqueda parcial por nombre del trabajador<br/>"
        "• Checador (Serial): Filtrar por dispositivo específico<br/>"
        "• Rango de fechas: Desde - Hasta",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Información mostrada:</b> Número de trabajador, nombre, fecha, hora exacta de checada "
        "y serial del dispositivo que la registró. Por defecto muestra los registros más recientes.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Trabajadores
    story.append(Paragraph("3. Módulo de Trabajadores", styles['Seccion']))
    story.append(Paragraph(
        "Gestión completa del personal. Es la base fundamental para el control de asistencias, "
        "ya que vincula los registros del checador con los horarios y departamentos.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Campos de cada trabajador:</b><br/>"
        "• <b>Número de trabajador:</b> Identificador único. DEBE coincidir con el ID registrado en el checador.<br/>"
        "• <b>Nombre completo:</b> Nombre y apellidos<br/>"
        "• <b>Departamento:</b> Área a la que pertenece (debe existir previamente)<br/>"
        "• <b>Tipo de plaza:</b> DOCENTE o ADMINISTRATIVO. <u>Importante:</u> Los docentes tienen reglas "
        "diferentes de salida (sin tolerancia para salir antes).<br/>"
        "• <b>Correo electrónico:</b> Para envío automático de reportes de bitácora",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Importar CSV:</b> Formato: num_trabajador,nombre,departamento,tipo_plaza,correo<br/>"
        "El departamento debe existir previamente en el sistema.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Departamentos
    story.append(Paragraph("4. Módulo de Departamentos", styles['Seccion']))
    story.append(Paragraph(
        "Organización del personal en áreas o departamentos. Facilita la segmentación de reportes "
        "y el procesamiento masivo de bitácoras por área.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Uso:</b> Cree los departamentos ANTES de agregar trabajadores. Se utilizan para:<br/>"
        "• Asignar trabajadores a un área específica<br/>"
        "• Filtrar reportes de bitácora por departamento<br/>"
        "• Procesar bitácoras masivas de un área completa<br/>"
        "<b>Importar CSV:</b> Formato: nombre,descripcion",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(PageBreak())
    
    # Horarios
    story.append(Paragraph("5. Módulo de Horarios", styles['Seccion']))
    story.append(Paragraph(
        "Creación de plantillas de horarios y asignación a trabajadores por periodo (semestre). "
        "El sistema usa estas asignaciones para calcular las incidencias en la bitácora.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Tab 1 - Plantillas de Horarios:</b><br/>"
        "Define los horarios base con entrada/salida por día de la semana.<br/>"
        "• <b>Formato simple:</b> 08:00-16:00 (una entrada, una salida)<br/>"
        "• <b>Formato mixto:</b> 08:00-12:00,14:00-16:00 (dos bloques con hora de comida)<br/>"
        "• <b>Descanso:</b> 00:00-00:00 para días sin trabajo",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Tab 2 - Asignaciones:</b><br/>"
        "Vincula una plantilla de horario con un trabajador específico.<br/>"
        "• Seleccionar trabajador y plantilla de horario<br/>"
        "• Definir fecha inicio y fecha fin (vigencia del horario)<br/>"
        "• Seleccionar semestre (Enero-Junio o Agosto-Diciembre)<br/>"
        "• El sistema detecta traslapes y no permite dos asignaciones activas para el mismo periodo",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Importar CSV:</b> Formato: num_trabajador,nombre_plantilla,fecha_inicio,fecha_fin,semestre<br/>"
        "Fechas en formato DD/MM/YYYY o DD/MM/YY",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Bitácora
    story.append(Paragraph("6. Módulo de Bitácora", styles['Seccion']))
    story.append(Paragraph(
        "Módulo principal del sistema. Procesa las checadas contra los horarios asignados y calcula "
        "automáticamente los códigos de incidencia. Genera reportes en PDF y permite envío por correo.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Modos de procesamiento:</b><br/>"
        "• <b>Individual:</b> Selecciona un trabajador y rango de fechas. Ideal para consultas específicas.<br/>"
        "• <b>Masivo:</b> Procesa todos los trabajadores de un departamento. Útil para reportes quincenales.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Columnas del reporte:</b><br/>"
        "• Fecha y día de la semana<br/>"
        "• Horario asignado (entrada-salida esperada)<br/>"
        "• Checadas registradas (1, 2, 3, 4 para horarios mixtos)<br/>"
        "• <b>Código:</b> A, R-, R+, F, O, ST, J, L (ver sección de códigos)<br/>"
        "• <b>Movimientos:</b> NA, FH o nomenclatura del movimiento registrado<br/>"
        "• Minutos de retardo y horas trabajadas",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Funciones adicionales:</b><br/>"
        "• <b>Resumen semanal:</b> Totales de A, R-, R+, F, O, ST por semana<br/>"
        "• <b>Descargar PDF:</b> Genera documento con formato oficial institucional<br/>"
        "• <b>Enviar por correo:</b> Envía el PDF al correo del trabajador (requiere configuración SMTP)",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Movimientos
    story.append(Paragraph("7. Módulo de Movimientos", styles['Seccion']))
    story.append(Paragraph(
        "Registro de incidencias especiales que justifican ausencias o modifican el registro automático. "
        "Los movimientos tienen PRIORIDAD sobre el cálculo automático de la bitácora.",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Tab 1 - Tipos de Movimientos (Catálogo):</b><br/>"
        "Define los códigos disponibles para registrar incidencias.<br/>"
        "• <b>Nomenclatura:</b> Código único (ej: COM001, PER-MED, INC001)<br/>"
        "• <b>Nombre:</b> Descripción corta (Comisión oficial, Permiso médico)<br/>"
        "• <b>Categoría:</b> Comisión, Permiso, Incapacidad, Licencia, Otros<br/>"
        "• <b>Letra:</b> Símbolo que aparece en bitácora: J (Justificado), L (Licencia), A (Autorizado)",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Tab 2 - Movimientos Realizados:</b><br/>"
        "Registra los movimientos aplicados a trabajadores específicos.<br/>"
        "• <b>Individual:</b> Selecciona trabajador, tipo, fecha y observaciones<br/>"
        "• <b>Asignación masiva:</b> Aplica el mismo movimiento a múltiples trabajadores a la vez",
        styles['TextoNormal']
    ))
    story.append(Paragraph(
        "<b>Efecto en bitácora:</b> Si existe un movimiento para un día, el código de incidencia "
        "cambia según la letra del tipo (J, L, A), independientemente de si hay checadas o no. "
        "La nomenclatura aparece en la columna 'Movimientos'.",
        styles['TextoNormal']
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # CONFIGURACIÓN TÉCNICA
    # ==========================================
    story.append(Paragraph("Configuración Técnica", styles['Subtitulo']))
    
    story.append(Paragraph("Detección de checadas duplicadas:", styles['Seccion']))
    story.append(Paragraph(
        "El sistema detecta y elimina checadas duplicadas automáticamente. Si dos checadas "
        "tienen menos de 60 segundos de diferencia, solo se registra la primera. "
        "Ejemplo: 09:16:00 y 09:16:56 se consideran la misma checada.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Horarios mixtos:", styles['Seccion']))
    story.append(Paragraph(
        "Para horarios con dos bloques (ej: 08:00-12:00, 14:00-16:00), el sistema valida "
        "cada bloque por separado y considera los retardos de ambas entradas.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Prioridad de movimientos:", styles['Seccion']))
    story.append(Paragraph(
        "Los movimientos registrados (permisos, incapacidades, etc.) tienen prioridad sobre "
        "el cálculo automático. Si existe un movimiento para el día, el código de incidencia "
        "cambia según la letra del movimiento, independientemente de las checadas.",
        styles['TextoNormal']
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # FUNDAMENTO REGLAMENTARIO
    # ==========================================
    story.append(Paragraph("Fundamento Reglamentario", styles['Subtitulo']))
    
    story.append(Paragraph(
        "Las reglas implementadas en el sistema están basadas en los reglamentos oficiales "
        "del Tecnológico Nacional de México (TECNM) y la Secretaría de Educación Pública (SEP).",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Jerarquía de reglamentos
    story.append(Paragraph("Jerarquía y Aplicabilidad de Reglamentos", styles['Seccion']))
    
    story.append(Paragraph(
        "Existen varios reglamentos que regulan la asistencia del personal. A continuación se explica "
        "cuál aplica a cada tipo de trabajador y su nivel de importancia:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    jerarquia_data = [
        ['Nivel', 'Reglamento', 'Aplica a'],
        ['1 (Base)', 'Reglamento de Condiciones Generales\nde Trabajo del Personal de la SEP', 'Todos los trabajadores\n(marco nacional)'],
        ['2', 'Reglamento Interior de Trabajo del\nPersonal DOCENTE de los IT', 'Solo Personal Docente\n(profesores)'],
        ['2', 'Reglamento Interior de Trabajo del\nPersonal NO DOCENTE de los IT', 'Solo Personal Administrativo\n(apoyo y asistencia)'],
    ]
    
    story.append(crear_tabla(jerarquia_data, col_widths=[0.8*inch, 3.2*inch, 2.3*inch]))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>¿Cuál tiene más importancia?</b> El Reglamento de la SEP es el marco general. Los reglamentos "
        "específicos del TECNM (Docentes y No Docentes) detallan las reglas para cada tipo de personal, "
        "pero no pueden contradecir el reglamento base de la SEP.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>¿Y el Sindicato (SNTE/Sección 61)?</b> El sindicato negocia el Contrato Colectivo de Trabajo "
        "y puede acordar condiciones adicionales, pero no genera reglamentos. Las reglas de asistencia "
        "están definidas en los reglamentos oficiales de la SEP y TECNM.",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Artículos por tipo de personal
    story.append(Paragraph("Artículos Aplicables por Tipo de Personal", styles['Seccion']))
    
    articulos_data = [
        ['Concepto', 'Personal Docente', 'Personal No Docente'],
        ['Tolerancia entrada (10 min)', 'Art. 153a TECNM\nArt. 80 SEP', 'Art. 98 Reg. No Docentes\nArt. 36 SEP'],
        ['Retardo Menor (11-20 min)', 'Art. 153a TECNM\nArt. 80a SEP', 'Art. 80a SEP'],
        ['Retardo Mayor (21-30 min)', 'Art. 153b TECNM\nArt. 80b SEP', 'Art. 80b SEP'],
        ['Falta por retardo (>30 min)', 'Art. 153c TECNM\nArt. 80c SEP', 'Art. 99 Reg. No Docentes'],
        ['Ventana entrada temprana', 'No especificado', 'Art. 103a (20 min antes)'],
        ['Tolerancia salida temprana', 'No especificado', 'Art. 103b (5 min antes)'],
        ['Ventana salida tardía', 'No especificado', 'Art. 103b (20 min después)'],
        ['No registrar salida', 'No especificado', 'Art. 102 (abandono)'],
    ]
    
    story.append(crear_tabla(articulos_data, col_widths=[2.2*inch, 2*inch, 2.1*inch]))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Nota importante:</b> El reglamento de Docentes NO tiene reglas específicas de salida. "
        "Las restricciones de salida que aplica el sistema para docentes (sin tolerancia) son una "
        "adaptación institucional basada en que los docentes deben cumplir el tiempo completo de sus clases.",
        styles['Referencia']
    ))
    
    story.append(PageBreak())
    
    # Extractos textuales
    story.append(Paragraph("Extractos Textuales de los Reglamentos", styles['Seccion']))
    
    extractos = [
        ("Artículo 80 - Reglamento de Condiciones Generales de Trabajo (SEP)",
         "\"El personal dispondrá de un máximo de diez minutos de tolerancia para el registro de asistencia. "
         "a) De 11 a 20 minutos se considera retardo menor y dos retardos en el mes constituyen una nota mala. "
         "b) De 21 a 30 minutos retardo mayor, cada uno constituye una nota mala. "
         "c) Después de 30 minutos se considerará falta de asistencia. "
         "d) Cinco notas malas dan lugar a un día de suspensión sin goce de sueldo.\""),
        
        ("Artículo 153 - Reglamento Interior de Trabajo del Personal Docente (TECNM)",
         "\"a) Se considera retardo menor cuando el trabajador registra su asistencia después de los "
         "primeros 10 minutos y hasta 20 minutos; dos retardos menores en un mes constituyen una nota mala. "
         "b) Se considera retardo mayor cuando registra después de los 20 minutos y hasta 30 minutos; "
         "cada retardo mayor constituye una nota mala. "
         "c) Después de los 30 minutos se considerará falta de asistencia.\""),
        
        ("Artículo 99 - Reglamento Interior de Trabajo del Personal No Docente",
         "\"Transcurridos los 30 minutos posteriores a la hora fijada para la iniciación de las labores, "
         "NO SE PERMITIRÁ A NINGÚN EMPLEADO REGISTRAR SU ASISTENCIA, por considerarse el caso como "
         "FALTA INJUSTIFICADA, sin derecho al salario correspondiente.\""),
        
        ("Artículo 103 - Reglamento Interior de Trabajo del Personal No Docente",
         "\"El trabajador no debe registrar su asistencia: "
         "a) Más de 20 minutos antes de su hora de entrada, excepto con autorización del jefe inmediato. "
         "b) Más de 5 minutos antes de su hora de salida o más de 20 minutos después de la misma, "
         "excepto que haya sido autorizado por su jefe inmediato superior.\""),
        
        ("Artículo 60 - Reglamento de Condiciones Generales de Trabajo (SEP)",
         "\"El abandono de empleo se considerará consumado al cuarto día después de que el trabajador "
         "haya faltado tres días consecutivos sin aviso ni causa justificada. También se considera abandono "
         "si faltare un día después de haber dejado de concurrir en ocho ocasiones en los 30 días anteriores.\""),
    ]
    
    for titulo, texto in extractos:
        story.append(Paragraph(f"<b>{titulo}</b>", styles['TextoNormal']))
        story.append(Paragraph(texto, styles['Referencia']))
        story.append(Spacer(1, 0.12*inch))
    
    story.append(PageBreak())
    
    # Dónde descargar los reglamentos
    story.append(Paragraph("Dónde Consultar los Reglamentos Oficiales", styles['Seccion']))
    
    story.append(Paragraph(
        "Los reglamentos oficiales están disponibles en los siguientes sitios institucionales:",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>Reglamento de Condiciones Generales de Trabajo de la SEP:</b>", styles['TextoNormal']))
    story.append(Paragraph(
        "Portal de la SEP → Normatividad → Reglamentos<br/>"
        "https://www.sep.gob.mx/es/sep1/Reglamentos<br/>"
        "Buscar: \"Reglamento de las Condiciones Generales de Trabajo del Personal de la SEP\"",
        styles['Referencia']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Reglamentos del Personal Docente y No Docente del TECNM:</b>", styles['TextoNormal']))
    story.append(Paragraph(
        "Portal del TecNM → Normatividad<br/>"
        "https://www.tecnm.mx/menu/normatividad<br/>"
        "Buscar: \"Reglamento Interior de Trabajo\" (Docente o No Docente)",
        styles['Referencia']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>También disponibles en:</b>", styles['TextoNormal']))
    story.append(Paragraph(
        "• Departamento de Recursos Humanos de tu instituto<br/>"
        "• Sección Sindical (SNTE) - Para consulta y asesoría<br/>"
        "• Dirección General de Personal de la SEP",
        styles['Referencia']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "<b>Recomendación:</b> Mantén una copia de los reglamentos aplicables en tu área. "
        "Ante cualquier duda sobre la aplicación de una regla, consulta directamente el artículo "
        "correspondiente en el reglamento oficial.",
        styles['TextoDestacado']
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # FLUJO DE TRABAJO
    # ==========================================
    story.append(Paragraph("Flujo de Trabajo Recomendado", styles['Subtitulo']))
    
    story.append(Paragraph("Configuración inicial (una vez):", styles['Seccion']))
    story.append(Paragraph(
        "1. Configurar checadores (IPs y ubicaciones)<br/>"
        "2. Crear departamentos<br/>"
        "3. Registrar trabajadores<br/>"
        "4. Crear plantillas de horarios<br/>"
        "5. Asignar horarios a trabajadores<br/>"
        "6. Crear tipos de movimientos comunes",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Operación diaria/semanal:", styles['Seccion']))
    story.append(Paragraph(
        "1. Descargar checadas de los dispositivos (diario o según necesidad)<br/>"
        "2. Registrar movimientos especiales (permisos, incapacidades)<br/>"
        "3. Procesar bitácora (semanal, quincenal o mensual)<br/>"
        "4. Revisar incidencias y corregir si es necesario<br/>"
        "5. Generar y enviar reportes",
        styles['TextoNormal']
    ))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Mantenimiento:", styles['Seccion']))
    story.append(Paragraph(
        "• Actualizar asignaciones de horarios cada semestre<br/>"
        "• Verificar correos de trabajadores estén actualizados<br/>"
        "• Revisar conexión de checadores periódicamente<br/>"
        "• Respaldar base de datos regularmente",
        styles['TextoNormal']
    ))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Pie de página
    fecha_gen = datetime.now().strftime("%d/%m/%Y")
    story.append(Paragraph(
        f"TecnoTime - Sistema de Gestión de Asistencias | Manual de Administración | Generado: {fecha_gen}",
        styles['PiePagina']
    ))
    
    # Generar PDF
    doc.build(story)
    print("✅ Generado: plantilla.pdf")


if __name__ == "__main__":
    print("Generando PDFs de documentación...")
    print()
    generar_plantilla_trabajadores()
    generar_plantilla_sistema()
    print()
    print("¡Listo! Los PDFs han sido actualizados con las nuevas reglas.")
