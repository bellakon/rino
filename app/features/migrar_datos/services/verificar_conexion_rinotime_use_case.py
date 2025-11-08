"""
Caso de uso: Verificar conexión a RinoTime
Responsabilidad: Verificar que se puede conectar a la base de datos RinoTime (biotimedb)
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_sync_connection
from app.config.database_config import DatabaseConfig


class VerificarConexionRinoTimeUseCase:
    """Verifica la conexión a la base de datos RinoTime"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_sync_connection)
    
    def ejecutar(self):
        """
        Verifica la conexión a RinoTime
        
        Returns:
            tuple: (info_conexion, error)
                info_conexion: dict con información de la BD
                error: mensaje de error si falla
        """
        try:
            # Verificar conexión con query simple usando QueryExecutor
            result, error = self.query_executor.ejecutar("SELECT 1 as test")
            if error:
                return None, f"No se pudo establecer conexión con RinoTime: {error}"
            
            # Obtener información de la base de datos
            db_info, error = self.query_executor.ejecutar("SELECT DATABASE() as db_name")
            if error:
                return None, error
            
            # Verificar que existe la tabla iclock_transaction
            table_check, error = self.query_executor.ejecutar("""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = 'iclock_transaction'
            """)
            
            if error:
                return None, error
            
            table_exists = table_check[0]['count'] > 0 if table_check else False
            
            # Contar registros en iclock_transaction
            registros_rinotime = 0
            if table_exists:
                result, error = self.query_executor.ejecutar("SELECT COUNT(*) as total FROM iclock_transaction")
                if not error and result:
                    registros_rinotime = result[0]['total']
            
            # Obtener configuración de DatabaseConfig
            sync_config = DatabaseConfig.get_connection_params('sync')
            
            info = {
                'conectado': True,
                'base_datos': db_info[0]['db_name'] if db_info else 'Desconocida',
                'tabla_existe': table_exists,
                'registros_rinotime': registros_rinotime,
                'host': sync_config['host'],
                'puerto': sync_config['port']
            }
            
            return info, None
            
        except Exception as e:
            return None, f"Error al conectar con RinoTime: {str(e)}"


# Instancia singleton
verificar_conexion_rinotime_use_case = VerificarConexionRinoTimeUseCase()
