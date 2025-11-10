"""
Configuración de letras para tipos de movimientos
"""

# Letras disponibles para clasificar tipos de movimientos
LETRAS_MOVIMIENTOS = [
    {'value': 'J', 'label': 'J - Justificación'},
    {'value': 'L', 'label': 'L - Licencia'},
    {'value': 'A', 'label': 'A - Especial'},
]

def get_letras_values():
    """Retorna solo los valores de las letras"""
    return [letra['value'] for letra in LETRAS_MOVIMIENTOS]

def get_letra_label(value):
    """Retorna el label de una letra específica"""
    for letra in LETRAS_MOVIMIENTOS:
        if letra['value'] == value:
            return letra['label']
    return value
