"""
Configuración base de la aplicación
Solo configuración de Flask y secretos
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración general de la aplicación Flask"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Servidor
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', '5000'))
