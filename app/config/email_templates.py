"""
Plantillas de correo electrónico configurables
Estas plantillas se usan para generar correos con contenido dinámico

VARIABLES DISPONIBLES PARA BINDING:
- {nombre} - Nombre completo del trabajador
- {num_trabajador} - Número de empleado
- {departamento} - Departamento de adscripción
- {periodo_inicio} - Fecha inicio del periodo
- {periodo_fin} - Fecha fin del periodo
- {total_dias} - Total de días procesados
- {quincena} - Número de quincena (1 o 2)
- {mes} - Nombre del mes
- {anio} - Año
- {fecha_limite_justificaciones} - Fecha límite para entregar justificaciones
- {descripcion_quincena} - Ej: "Primera quincena de Noviembre"
- {remitente_nombre} - Nombre de quien envía
- {remitente_departamento} - Departamento del remitente
"""

from pathlib import Path
import json

# Ruta base para recursos de correo (imágenes, etc.)
EMAIL_RESOURCES_PATH = Path(__file__).parent.parent.parent / 'email_resources'

# Ruta del archivo de configuración persistente
EMAIL_SETTINGS_PATH = Path(__file__).parent / 'email_settings.json'

# =============================================================================
# FUNCIONES PARA CONFIGURACIÓN PERSISTENTE
# =============================================================================

def cargar_configuracion() -> dict:
    """Carga la configuración de plantillas desde archivo JSON"""
    config_default = {
        'usar_plantilla_html': True,
        'imagen_encabezado': '',
        'imagen_secundaria': '',
        'remitente_nombre': 'PREFECTURA RECURSOS HUMANOS',
        'remitente_departamento': 'Depto. de Recursos Humanos'
    }
    
    try:
        if EMAIL_SETTINGS_PATH.exists():
            with open(EMAIL_SETTINGS_PATH, 'r', encoding='utf-8') as f:
                config = json.load(f)
                config_default.update(config)
    except Exception as e:
        print(f"Error cargando configuración de email: {e}")
    
    return config_default


def guardar_configuracion(config: dict) -> tuple:
    """Guarda la configuración de email en archivo JSON"""
    try:
        with open(EMAIL_SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True, None
    except Exception as e:
        return False, str(e)


# =============================================================================
# CONFIGURACIÓN GLOBAL DE CORREOS (cargada dinámicamente)
# =============================================================================
def obtener_config() -> dict:
    """Obtiene la configuración actual (combinación de defaults + persistente)"""
    return cargar_configuracion()


# EMAIL_CONFIG ahora es una función que carga dinámicamente
# Para compatibilidad, lo dejamos como variable que se actualiza
EMAIL_CONFIG = cargar_configuracion()

# =============================================================================
# PLANTILLA: REPORTE DE ASISTENCIA (con HTML enriquecido)
# =============================================================================
REPORTE_ASISTENCIA_EMAIL = {
    'asunto': 'REPORTE DE ASISTENCIA - {nombre}',
    'usa_html': True,
    'imagenes_embebidas': ['imagen_encabezado', 'imagen_secundaria'],  # claves de EMAIL_CONFIG
    'adjuntos': ['plantilla_trabajadores.pdf'],  # Archivos a adjuntar
    'cuerpo_html': '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: Aptos, Calibri, Helvetica, sans-serif;
        font-size: 12pt;
        color: #000000;
        background-color: #ffffff;
        margin: 0;
        padding: 20px;
    }}
    .container {{
        max-width: 700px;
        margin: 0 auto;
    }}
    .header {{
        text-align: center;
        margin-bottom: 20px;
    }}
    .header img {{
        max-width: 160px;
        height: auto;
    }}
    .content {{
        text-align: center;
    }}
    .mensaje-principal {{
        font-size: 16pt;
        margin: 20px 0;
    }}
    .periodo {{
        font-size: 16pt;
        color: #3b204d;
        background-color: #ffc080;
        padding: 10px;
        display: inline-block;
        font-weight: bold;
    }}
    .acuse {{
        font-size: 18pt;
        color: #ffffff;
        background-color: #ff0000;
        padding: 10px 20px;
        display: inline-block;
        margin: 15px 0;
    }}
    .fecha-limite {{
        font-size: 16pt;
        color: #5c327c;
        font-weight: bold;
        font-style: italic;
        margin: 15px 0;
    }}
    .recordatorio {{
        font-size: 16pt;
        color: #002451;
        font-weight: bold;
        margin: 20px 0;
    }}
    .notas {{
        text-align: left;
        margin: 20px 0;
    }}
    .notas h3 {{
        font-size: 14pt;
        margin-bottom: 10px;
    }}
    .notas ul {{
        margin-left: 20px;
    }}
    .notas li {{
        font-size: 14pt;
        margin-bottom: 10px;
        line-height: 1.4;
    }}
    .highlight-yellow {{
        background-color: #ffff00;
        text-decoration: underline;
    }}
    .highlight-cyan {{
        background-color: #00ffff;
        text-decoration: underline;
    }}
    .tabla-codigos {{
        border-collapse: collapse;
        margin: 20px auto;
        font-size: 12pt;
    }}
    .tabla-codigos th, .tabla-codigos td {{
        border: 1px solid #ababab;
        padding: 8px 12px;
        text-align: center;
    }}
    .tabla-codigos th {{
        background-color: #ababab;
    }}
    .tabla-codigos tr:nth-child(even) {{
        background-color: rgba(171, 171, 171, 0.14);
    }}
    .firma {{
        text-align: center;
        margin-top: 30px;
        font-size: 12pt;
    }}
</style>
</head>
<body>
<div class="container">
    <!-- ENCABEZADO CON LOGOS -->
    <div class="header">
        <img src="cid:imagen_encabezado" alt="Logo Institucional">
        <br><br>
        <img src="cid:imagen_secundaria" alt="Banner">
    </div>
    
    <!-- CONTENIDO PRINCIPAL -->
    <div class="content">
        <p class="mensaje-principal">
            Por medio del presente hago llegar su Reporte de Asistencias de la:
        </p>
        
        <p class="periodo">
            {descripcion_quincena}
        </p>
        
        <p class="acuse">
            Solicitamos su <b>acuse de recibido</b>.
        </p>
        
        <p class="fecha-limite">
            Se recibirán justificaciones hasta el {fecha_limite_justificaciones}.
        </p>
        
        <p class="recordatorio">
            Recuerda: Si entregas Constancias de Tiempo ISSSTE, Órdenes de traslado, 
            Licencias Médicas, etc. colocarles tu número de empleado y departamento de adscripción.
        </p>
    </div>
    
    <!-- NOTAS IMPORTANTES -->
    <div class="notas">
        <h3>NOTAS:</h3>
        <ul>
            <li>Las omisiones de checada se deben justificar al día siguiente de la incidencia, 
                de acuerdo al art. 102 del <b>REGLAMENTO INTERNO DE TRABAJO DEL PERSONAL NO DOCENTE 
                DE LOS INSTITUTOS TECNOLÓGICOS.</b></li>
            <li><span class="highlight-yellow">Entregar las Licencias Médicas a no más tardar a 48 horas 
                después de su licencia emitida, esto de acuerdo al art. 109 inciso b.</span></li>
            <li>LAS INCIDENCIAS O JUSTIFICANTES ENTREGADOS DESPUÉS DEL 01 DE SEPTIEMBRE AÚN NO SE VERÁN 
                REFLEJADOS EN ESTE REPORTE. SI DESEA NUEVAMENTE SU REPORTE CON SUS JUSTIFICACIONES 
                REFLEJADAS SOLICITARLO POR ESTE MEDIO.</li>
        </ul>
    </div>
    
    <!-- TABLA DE CÓDIGOS DE JUSTIFICACIÓN -->
    <div class="notas">
        <p>Si ha realizado justificaciones dentro de la quincena 
           <span class="highlight-cyan">ADJUNTO LOS CÓDIGOS QUE PODRÍAN APLICARSE PARA GENERAR EN SUS JUSTIFICANTES:</span>
        </p>
    </div>
    
    <table class="tabla-codigos">
        <tr>
            <th>NOMBRE</th>
            <th>JUSTIFICACIÓN</th>
            <th>NOMENCLATURA</th>
        </tr>
        <tr><td>AJUSTE DE HORARIO</td><td>J</td><td>AH</td></tr>
        <tr><td>CONSTANCIA DE CUIDADOS MATERNOS</td><td>J</td><td>CCM</td></tr>
        <tr><td>CONSTANCIA DE HOSPITALIZACIÓN</td><td>J</td><td>COH</td></tr>
        <tr><td>COMISIÓN EXTERNA</td><td>J</td><td>COM</td></tr>
        <tr><td>COMISIÓN INTERNA</td><td>J</td><td>CI</td></tr>
        <tr><td>COMPENSACIÓN DE TIEMPO</td><td>J</td><td>CT</td></tr>
        <tr><td>CONSTANCIA DE TIEMPO ISSSTE</td><td>J</td><td>CTI</td></tr>
        <tr><td>PERMISO DE LACTANCIA</td><td>P</td><td>LAC</td></tr>
        <tr><td>PERMISO ECONÓMICO</td><td>P</td><td>ECO</td></tr>
        <tr><td>CONST. DE ACOMPAÑAMIENTO DIRECTO</td><td>J</td><td>CCF</td></tr>
        <tr><td>ORDEN DE TRASLADO</td><td>L</td><td>OT</td></tr>
        <tr><td>SUSPENSIÓN OFICIAL</td><td>J</td><td>SO</td></tr>
        <tr><td>LICENCIA SINDICAL</td><td>L</td><td>LS</td></tr>
        <tr><td>PERMISO DE PATERNIDAD</td><td>P</td><td>PP</td></tr>
        <tr><td>CUIDADOS MATERNOS</td><td>L</td><td>MAT</td></tr>
        <tr><td>PERIODO SABÁTICO</td><td>L</td><td>SAB</td></tr>
        <tr><td>VACACIONES OFICIALES</td><td>V</td><td>VAC</td></tr>
        <tr><td>REP. DE TIEMPO POR INCP</td><td>J</td><td>REP</td></tr>
        <tr><td>CONSTANCIA CONSULTA ISSSTE EXTERNA</td><td>J</td><td>CIE</td></tr>
        <tr><td>SUSPENSIÓN LOCAL</td><td>J</td><td>SL</td></tr>
        <tr><td>LICENCIA POR MATRIMONIO</td><td>L</td><td>LM</td></tr>
        <tr><td>CONSTANCIA ISSSTE</td><td>J</td><td>C</td></tr>
        <tr><td>JUSTIFICACIÓN POR JEFE</td><td>J</td><td>JPJ</td></tr>
        <tr><td>SUSPENSIÓN POR CLIMA</td><td>J</td><td>SPC</td></tr>
        <tr><td>PRE NACIONAL TIZIMÍN</td><td>J</td><td>PRT</td></tr>
        <tr><td>NACIONAL</td><td>J</td><td>NAS</td></tr>
        <tr><td>BLINDAJE ELECTORAL</td><td>J</td><td>BLE</td></tr>
        <tr><td>VOTACIÓN SINDICAL</td><td>J</td><td>VS</td></tr>
        <tr><td>DILIGENCIA SINDICAL</td><td>J</td><td>DV</td></tr>
    </table>
    
    <!-- FIRMA -->
    <div class="firma">
        <p><b>{remitente_nombre}</b></p>
        <p>{remitente_departamento}</p>
    </div>
</div>
</body>
</html>''',
    # Versión texto plano (fallback)
    'cuerpo_texto': '''
Estimado(a) {nombre},

Por medio del presente hago llegar su Reporte de Asistencias de la:
{descripcion_quincena}

Solicitamos su acuse de recibido.
Se recibirán justificaciones hasta el {fecha_limite_justificaciones}.

Recuerda: Si entregas Constancias de Tiempo ISSSTE, Órdenes de traslado, 
Licencias Médicas, etc. colocarles tu número de empleado y departamento de adscripción.

NOTAS:
- Las omisiones de checada se deben justificar al día siguiente de la incidencia.
- Entregar las Licencias Médicas a no más tardar a 48 horas después de su licencia emitida.

Atentamente,
{remitente_nombre}
{remitente_departamento}
'''
}

# =============================================================================
# PLANTILLA: BITÁCORA DE ASISTENCIAS (simplificada)
# =============================================================================
BITACORA_EMAIL = {
    'asunto': 'Bitácora de Asistencias - {nombre} ({num_trabajador})',
    'usa_html': False,
    'adjuntos': ['plantilla_trabajadores.pdf'],
    'cuerpo_texto': '''Estimado(a) {nombre},

Adjunto encontrará su bitácora de asistencias correspondiente al periodo:

📅 Fecha Inicio: {periodo_inicio}
📅 Fecha Fin: {periodo_fin}
📊 Total de días procesados: {total_dias}

Este reporte incluye sus registros de entrada y salida, horas trabajadas y cualquier incidencia registrada durante el periodo indicado.

Si tiene alguna pregunta o requiere aclaración sobre algún registro, favor de contactar al departamento de Recursos Humanos.

Saludos cordiales,
{remitente_nombre}
{remitente_departamento}'''
}

# =============================================================================
# PLANTILLA: NÓMINA (ejemplo para futuro)
# =============================================================================
NOMINA_EMAIL = {
    'asunto': 'Nómina {periodo} - {nombre}',
    'usa_html': False,
    'cuerpo_texto': '''Estimado(a) {nombre},

Adjunto encontrará su recibo de nómina correspondiente al periodo {periodo}.

Saludos cordiales,
{remitente_nombre}
{remitente_departamento}'''
}

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def obtener_ruta_imagen(nombre_imagen: str) -> Path:
    """Obtiene la ruta completa de una imagen de email"""
    return EMAIL_RESOURCES_PATH / nombre_imagen

def obtener_ruta_adjunto(nombre_archivo: str) -> Path:
    """Obtiene la ruta completa de un archivo adjunto"""
    # Buscar primero en el directorio raíz del proyecto
    ruta_raiz = Path(__file__).parent.parent.parent / nombre_archivo
    if ruta_raiz.exists():
        return ruta_raiz
    # Si no existe, buscar en email_resources
    return EMAIL_RESOURCES_PATH / nombre_archivo

def formatear_plantilla(plantilla: dict, variables: dict) -> dict:
    """
    Formatea una plantilla reemplazando las variables binding
    
    Args:
        plantilla: Diccionario de plantilla (ej: REPORTE_ASISTENCIA_EMAIL)
        variables: Diccionario con los valores a reemplazar
        
    Returns:
        Diccionario con asunto y cuerpo formateados
    """
    resultado = {}
    
    # Cargar configuración actual
    config = cargar_configuracion()
    
    # Aplicar valores por defecto de configuración
    variables_completas = {
        'remitente_nombre': config.get('remitente_nombre', 'Recursos Humanos'),
        'remitente_departamento': config.get('remitente_departamento', 'Depto. RH'),
    }
    variables_completas.update(variables)
    
    # Formatear asunto
    resultado['asunto'] = plantilla['asunto'].format(**variables_completas)
    
    # Formatear cuerpo (HTML o texto)
    if plantilla.get('usa_html') and 'cuerpo_html' in plantilla:
        resultado['cuerpo_html'] = plantilla['cuerpo_html'].format(**variables_completas)
        resultado['cuerpo_texto'] = plantilla.get('cuerpo_texto', '').format(**variables_completas)
        resultado['usa_html'] = True
    else:
        resultado['cuerpo_texto'] = plantilla.get('cuerpo_texto', '').format(**variables_completas)
        resultado['usa_html'] = False
    
    # Copiar lista de imágenes y adjuntos
    resultado['imagenes_embebidas'] = plantilla.get('imagenes_embebidas', [])
    resultado['adjuntos'] = plantilla.get('adjuntos', [])
    
    return resultado
