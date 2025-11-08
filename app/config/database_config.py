"""
Configuración de múltiples bases de datos
Sistema: Base de datos principal de la aplicación
Sync: Base de datos para sincronización de checadas
"""
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Configuración de conexiones a múltiples bases de datos"""
    
    # Base de datos SISTEMA (principal)
    SISTEMA = {
        'host': os.getenv('DB_SISTEMA_HOST', 'localhost'),
        'port': int(os.getenv('DB_SISTEMA_PORT', '3306')),
        'user': os.getenv('DB_SISTEMA_USER', 'root'),
        'password': os.getenv('DB_SISTEMA_PASSWORD', ''),
        'database': os.getenv('DB_SISTEMA_NAME', 'asistencias'),
        'charset': 'utf8mb4'
    }
    
    # Base de datos RINO TIME (sincronización de checadas)
    SYNC = {
        'host': os.getenv('DB_SYNC_HOST', 'localhost'),
        'port': int(os.getenv('DB_SYNC_PORT', '3306')),
        'user': os.getenv('DB_SYNC_USER', 'root'),
        'password': os.getenv('DB_SYNC_PASSWORD', ''),
        'database': os.getenv('DB_SYNC_NAME', 'checadas_sync'),
        'charset': 'utf8mb4'
    }
    
    @classmethod
    def get_connection_params(cls, db_type='sistema'):
        """
        Retorna parámetros de conexión según el tipo de BD
        
        Args:
            db_type (str): 'sistema' o 'sync'
            
        Returns:
            dict: Parámetros de conexión
        """
        if db_type.lower() == 'sync':
            return cls.SYNC.copy()
        return cls.SISTEMA.copy()
