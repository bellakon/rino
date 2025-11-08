"""
Conexión a múltiples bases de datos
Responsabilidad única: manejo de conexiones SQL a diferentes BD
"""
import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from app.config.database_config import DatabaseConfig


class DatabaseConnection:
    """Maneja conexiones a múltiples bases de datos"""
    
    def __init__(self, db_type='sistema'):
        """
        Inicializa la conexión para un tipo específico de BD
        
        Args:
            db_type (str): 'sistema' o 'sync'
        """
        self.db_type = db_type
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexión a la base de datos
        
        Yields:
            connection: Conexión a la base de datos
        """
        connection = None
        try:
            connection = pymysql.connect(**DatabaseConfig.get_connection_params(self.db_type))
            yield connection
            connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
    
    def verificar_conexion(self):
        """
        Verifica que la conexión funcione
        
        Returns:
            tuple: (True/False, error)
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    return True, None
        except Exception as e:
            return False, str(e)


# Instancias singleton para cada tipo de BD
db_connection = DatabaseConnection('sistema')      # BD principal del sistema
db_sync_connection = DatabaseConnection('sync')    # BD de sincronización
