"""
Ejecutor de queries SQL
Responsabilidad única: ejecutar consultas SQL personalizadas
Soporta múltiples conexiones de base de datos
"""
import pymysql
from pymysql.cursors import DictCursor
from app.core.database.connection import db_connection, db_sync_connection


class QueryExecutor:
    """Ejecuta queries SQL personalizadas en diferentes bases de datos"""
    
    def __init__(self, connection=None):
        """
        Inicializa el ejecutor con una conexión específica
        
        Args:
            connection: DatabaseConnection instance (default: db_connection)
        """
        self.connection = connection or db_connection
    
    def ejecutar(self, query, params=None):
        """
        Ejecuta una query SQL (SELECT, INSERT, UPDATE, DELETE)
        
        Args:
            query (str): Query SQL a ejecutar
            params (tuple/dict): Parámetros para la query
            
        Returns:
            tuple: (resultados, error)
        """
        try:
            with self.connection.get_connection() as conn:
                with conn.cursor(DictCursor) as cursor:
                    cursor.execute(query, params or ())
                    
                    # Si es SELECT, devolver resultados
                    if query.strip().upper().startswith('SELECT'):
                        resultados = cursor.fetchall()
                        return resultados, None
                    else:
                        # Para INSERT, UPDATE, DELETE
                        return {'affected_rows': cursor.rowcount}, None
                        
        except Exception as e:
            return None, str(e)
    
    def ejecutar_batch(self, query, params_list, ignore_duplicates=True):
        """
        Ejecuta una query múltiples veces con diferentes parámetros
        Útil para INSERTs múltiples con manejo de duplicados
        
        Args:
            query (str): Query SQL a ejecutar (típicamente INSERT)
            params_list (list): Lista de tuplas con parámetros
            ignore_duplicates (bool): Si True, ignora errores de duplicados
            
        Returns:
            tuple: (cantidad_insertada, error)
        """
        if not params_list:
            return 0, "No hay datos para procesar"
        
        try:
            with self.connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    registros_procesados = 0
                    
                    for params in params_list:
                        try:
                            cursor.execute(query, params)
                            registros_procesados += 1
                        except pymysql.IntegrityError as e:
                            if ignore_duplicates:
                                # Continuar con el siguiente registro
                                continue
                            else:
                                # Re-lanzar el error si no se ignoran duplicados
                                raise e
                    
                    return registros_procesados, None
                    
        except Exception as e:
            return 0, str(e)


# Instancias singleton para cada tipo de BD
query_executor = QueryExecutor(db_connection)           # BD Sistema (principal)
query_executor_sync = QueryExecutor(db_sync_connection) # BD Sync (sincronización)
