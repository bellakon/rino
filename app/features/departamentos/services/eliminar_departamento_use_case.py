"""
Caso de uso: Eliminar Departamento
Responsabilidad: Eliminar un departamento de la BD
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class EliminarDepartamentoUseCase:
    """Elimina un departamento"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_departamento):
        """
        Elimina un departamento
        
        Args:
            id_departamento: ID del departamento
            
        Returns:
            tuple: (success, error)
        """
        try:
            # Verificar si hay trabajadores asignados
            query_trabajadores = """
                SELECT COUNT(*) as total 
                FROM trabajadores 
                WHERE departamento_id = %s
            """
            resultado, error = self.query_executor.ejecutar(query_trabajadores, (id_departamento,))
            
            if error:
                return False, error
            
            if resultado and resultado[0]['total'] > 0:
                return False, f"No se puede eliminar. Hay {resultado[0]['total']} trabajadores asignados a este departamento"
            
            # Eliminar
            query = "DELETE FROM departamentos WHERE id = %s"
            _, error = self.query_executor.ejecutar(query, (id_departamento,))
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al eliminar departamento: {str(e)}"


# Instancia singleton
eliminar_departamento_use_case = EliminarDepartamentoUseCase()
