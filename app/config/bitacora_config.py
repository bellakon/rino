"""
Configuración de reglas para cálculo de incidencias en bitácora
"""

# ============================================
# CÓDIGOS DE INCIDENCIA (COLUMNA CÓDIGO)
# ============================================
CODIGOS_INCIDENCIA = {
    'A': 'Asistencia',
    'F': 'Falta',
    'R+': 'Retardo Mayor',
    'R-': 'Retardo Menor',
    'O': 'Omisión',
    'ST': 'Salida Temprana',
    'J': 'Justificado',
    'L': 'Licencia'
}

# ============================================
# TIPOS DE FALTA (COLUMNA MOVIMIENTOS)
# ============================================
TIPOS_FALTA = {
    'FNA': 'Falta - No marcó asistencia',
    'FRT': 'Falta por retardo excesivo (más de 30 min)',
    'FST': 'Falta por salida muy tardía (más de 30 min)',
    'FET': 'Falta - Entrada demasiado temprana'
}

# ============================================
# REGLAS DE TOLERANCIA (en minutos)
# ============================================

# Ventana de entrada temprana válida (antes de hora de entrada)
# Ejemplo: Si entrada es 8:00, puede checar desde 7:30 (30 minutos antes)
MINUTOS_ANTES_PERMITIDOS = 30

# Tolerancia de entrada (llegada normal sin incidencia)
# Ejemplo: Si entrada es 8:00, hasta 8:10 es asistencia normal
TOLERANCIA_ENTRADA_MINUTOS = 10

# Retardo menor (después de tolerancia pero antes de retardo mayor)
# Ejemplo: 8:11 a 8:16 es retardo menor
MINUTOS_RETARDO_MENOR_MIN = 11
MINUTOS_RETARDO_MENOR_MAX = 16

# Retardo mayor (grave pero no falta)
# Ejemplo: 8:17 a 8:30 es retardo mayor
MINUTOS_RETARDO_MAYOR_MIN = 17
MINUTOS_RETARDO_MAYOR_MAX = 30

# Más de este tiempo después de la hora de entrada = FALTA
# Ejemplo: 8:31 en adelante es falta por retardo
MINUTOS_FALTA = 31

# Tolerancia de salida (puede salir antes sin incidencia) - SOLO NO DOCENTES
# Ejemplo: Si salida es 16:00, puede salir desde 15:35 sin problema
TOLERANCIA_SALIDA_NO_DOCENTE_MINUTOS = 5

# Tolerancia de salida DOCENTES (deben checar exacto o después)
# Los docentes NO pueden salir antes de su hora de salida
TOLERANCIA_SALIDA_DOCENTE_MINUTOS = 0

# Máximo de minutos tarde para salida antes de ser FALTA
# Ejemplo: Si salida es 16:00, hasta 16:30 es válido, 16:31 es falta
MINUTOS_SALIDA_TARDE_MAX = 30

# ============================================
# DETECCIÓN DE CHECADAS DUPLICADAS
# ============================================
# Máximo de segundos entre checadas para considerarlas duplicadas
# Ejemplo: 09:16:00 y 09:16:56 (56 segundos) son la misma checada
SEGUNDOS_MAX_CHECADAS_DUPLICADAS = 60  # 1 minuto

# ============================================
# REGLAS POR TIPO DE PLAZA
# ============================================
TIPOS_PLAZA_DOCENTE = ['DOCENTE', 'PROFESOR', 'MAESTRO']

def es_docente(tipo_plaza: str) -> bool:
    """Determina si un tipo de plaza es docente"""
    if not tipo_plaza:
        return False
    return tipo_plaza.upper() in TIPOS_PLAZA_DOCENTE

# ============================================
# REGLAS DE OMISIÓN
# ============================================
# Omisión: Marcó entrada pero no salida (o viceversa)
# Se marca como 'O' en el código de incidencia

# ============================================
# FUNCIONES DE VALIDACIÓN
# ============================================

def validar_entrada_temprana(minutos_diferencia: int) -> bool:
    """
    Valida si una entrada temprana es válida
    
    Args:
        minutos_diferencia: Minutos ANTES de la hora de entrada (positivo)
    
    Returns:
        True si la entrada temprana es válida
    """
    return minutos_diferencia <= MINUTOS_ANTES_PERMITIDOS

def calcular_codigo_retardo(minutos_tarde: int) -> tuple:
    """
    Calcula el código de incidencia y tipo de falta según minutos de retardo
    
    Args:
        minutos_tarde: Minutos DESPUÉS de la hora de entrada
    
    Returns:
        tuple: (codigo_incidencia, tipo_falta)
        - codigo_incidencia: 'A', 'R-', 'R+', o 'F' (para columna Código)
        - tipo_falta: 'FRT' o None (para columna Movimientos)
    """
    if minutos_tarde <= TOLERANCIA_ENTRADA_MINUTOS:
        return ('A', None)  # Asistencia normal
    elif MINUTOS_RETARDO_MENOR_MIN <= minutos_tarde <= MINUTOS_RETARDO_MENOR_MAX:
        return ('R-', None)  # Retardo menor
    elif MINUTOS_RETARDO_MAYOR_MIN <= minutos_tarde <= MINUTOS_RETARDO_MAYOR_MAX:
        return ('R+', None)  # Retardo mayor
    else:
        return ('F', 'FRT')  # Falta por retardo excesivo

def validar_salida(minutos_diferencia: int, es_docente_plaza: bool) -> tuple:
    """
    Valida la hora de salida
    
    Args:
        minutos_diferencia: Positivo si salió tarde, negativo si salió temprano
        es_docente_plaza: True si es docente
    
    Returns:
        tuple: (codigo_incidencia, tipo_falta, descripcion)
    """
    # Salió tarde
    if minutos_diferencia > 0:
        if minutos_diferencia > MINUTOS_SALIDA_TARDE_MAX:
            return ('F', 'FST', f'Salida {minutos_diferencia} minutos tarde (más de {MINUTOS_SALIDA_TARDE_MAX} min)')
        else:
            return ('A', None, 'Asistencia (salida dentro de tolerancia)')
    
    # Salió temprano
    minutos_temprano = abs(minutos_diferencia)
    
    if es_docente_plaza:
        # Docentes NO pueden salir antes
        if minutos_temprano > TOLERANCIA_SALIDA_DOCENTE_MINUTOS:
            return ('ST', None, f'Salida temprana: {minutos_temprano} minutos antes')
        else:
            return ('A', None, 'Asistencia')
    else:
        # No docentes tienen tolerancia
        if minutos_temprano <= TOLERANCIA_SALIDA_NO_DOCENTE_MINUTOS:
            return ('A', None, 'Asistencia')
        else:
            return ('ST', None, f'Salida temprana: {minutos_temprano} minutos antes')

# ============================================
# DESCRIPCIÓN DE REGLAS (para mostrar al usuario)
# ============================================
DESCRIPCION_REGLAS = f"""
REGLAS DE INCIDENCIAS:

ENTRADA:
- Puede checar desde {MINUTOS_ANTES_PERMITIDOS} minutos antes de su hora de entrada
- Entrada más temprana que eso = FALTA
- Tolerancia: hasta {TOLERANCIA_ENTRADA_MINUTOS} minutos tarde = ASISTENCIA
- {MINUTOS_RETARDO_MENOR_MIN}-{MINUTOS_RETARDO_MENOR_MAX} minutos tarde = RETARDO MENOR (R-)
- {MINUTOS_RETARDO_MAYOR_MIN}-{MINUTOS_RETARDO_MAYOR_MAX} minutos tarde = RETARDO MAYOR (R+)
- Más de {MINUTOS_FALTA} minutos tarde = FALTA

SALIDA (NO DOCENTES):
- Puede salir hasta {TOLERANCIA_SALIDA_NO_DOCENTE_MINUTOS} minutos antes sin problema
- Más temprano = SALIDA TEMPRANA (ST)
- Hasta {MINUTOS_SALIDA_TARDE_MAX} minutos tarde = ASISTENCIA
- Más de {MINUTOS_SALIDA_TARDE_MAX} minutos tarde = FALTA

SALIDA (DOCENTES):
- Deben checar EXACTAMENTE a su hora o después
- Cualquier salida temprana = SALIDA TEMPRANA (ST)
- Hasta {MINUTOS_SALIDA_TARDE_MAX} minutos tarde = ASISTENCIA
- Más de {MINUTOS_SALIDA_TARDE_MAX} minutos tarde = FALTA

OMISIÓN:
- Marcó entrada pero NO salida = OMISIÓN (O)
- Marcó salida pero NO entrada = OMISIÓN (O)
"""
