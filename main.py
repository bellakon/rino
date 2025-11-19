"""
Punto de entrada principal de la aplicación Flask
Sistema de Gestión de Checadores ZKTeco
"""
from app import create_app
import os

# Crear la aplicación
app = create_app()

# Configurar la clave secreta para sesiones
app.secret_key = app.config.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuraciones para archivos grandes
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1 GB máximo
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == '__main__':
    # Obtener configuración
    from app.config.app_config import Config
    
    print("=" * 60)
    print("Sistema de Checadores ZKTeco")
    print("=" * 60)
    print(f"Servidor corriendo en: http://{Config.HOST}:{Config.PORT}")
    print(f"Modo debug: {Config.DEBUG}")
    print(f"Tamaño máximo de archivo: 1 GB")
    print("=" * 60)
    
    # Iniciar servidor con configuración optimizada
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        threaded=True,  # Habilitar threading
        request_handler=None  # Usar handler por defecto de Werkzeug
    )
