"""
Plantillas de correo electrónico configurables
Estas plantillas se usan para generar correos con contenido dinámico
"""

# Plantilla para correo de bitácora
BITACORA_EMAIL = {
    'asunto': 'Bitácora de Asistencias - {nombre} ({num_trabajador})',
    'cuerpo': '''Estimado(a) {nombre},

Adjunto encontrará su bitácora de asistencias correspondiente al periodo:

📅 Fecha Inicio: {periodo_inicio}
📅 Fecha Fin: {periodo_fin}
📊 Total de días procesados: {total_dias}

Este reporte incluye sus registros de entrada y salida, horas trabajadas y cualquier incidencia registrada durante el periodo indicado.

Si tiene alguna pregunta o requiere aclaración sobre algún registro, favor de contactar al departamento de Recursos Humanos.

Saludos cordiales,
Departamento de Recursos Humanos'''
}

# Plantilla para correo de nómina (ejemplo para futuro)
NOMINA_EMAIL = {
    'asunto': 'Nómina {periodo} - {nombre}',
    'cuerpo': '''Estimado(a) {nombre},

Adjunto encontrará su recibo de nómina correspondiente al periodo {periodo}.

Saludos cordiales,
Departamento de Nómina'''
}
