"""
Configuración de usuarios para autenticación básica
Agregar usuarios aquí con formato: {'username': 'contraseña'}
"""

# Lista de usuarios autorizados
# IMPORTANTE: En producción, considera usar hashing de contraseñas
USERS = {
    'admin': 'admin123',
    'prefectura': 'prefectura2025',
    'sistemas': 'sistemas2025',
}

# Tiempo de sesión en segundos (8 horas por defecto)
SESSION_LIFETIME_SECONDS = 8 * 60 * 60
