"""
Configuración de SMTP para envío de correos
Lee las credenciales desde el archivo .env
Ver instrucciones en CONFIGURACION_EMAIL.md
"""
import os

# Configuración del servidor SMTP
SMTP_CONFIG = {
    'host': os.getenv('SMTP_HOST'),
    'port': int(os.getenv('SMTP_PORT', 587)),
    'use_tls': os.getenv('SMTP_USE_TLS', 'True').lower() == 'true',
    'username': os.getenv('SMTP_USERNAME'),
    'password': os.getenv('SMTP_PASSWORD'),
    'from_email': os.getenv('SMTP_FROM_EMAIL'),
    'from_name': os.getenv('SMTP_FROM_NAME', 'Sistema de Recursos Humanos')
}

def validar_config():
    """Valida que la configuración SMTP esté completa"""
    if not SMTP_CONFIG['host']:
        return False, "❌ SMTP_HOST no está configurado en .env"
    
    if not SMTP_CONFIG['username']:
        return False, "❌ SMTP_USERNAME no está configurado en .env"
    
    if not SMTP_CONFIG['password']:
        return False, "❌ SMTP_PASSWORD no está configurado en .env"
    
    if not SMTP_CONFIG['from_email']:
        return False, "❌ SMTP_FROM_EMAIL no está configurado en .env"
    
    return True, "✅ Configuración SMTP completa"
