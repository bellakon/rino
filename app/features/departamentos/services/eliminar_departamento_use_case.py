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
            # No permitir eliminar el departamento "SIN ASIGNAR" (id=1)
            if id_departamento == 1:
                return False, "No se puede eliminar el departamento 'SIN ASIGNAR'"
            
            # Verificar si hay trabajadores asignados
            query_trabajadores = """
                SELECT COUNT(*) as total 
                FROM trabajadores 
                WHERE departamento_id = %s
            """
            resultado, error = self.query_executor.ejecutar(query_trabajadores, (id_departamento,))
            
            if error:
                return False, error
            
            # Si hay trabajadores asignados, reasignarlos al departamento "SIN ASIGNAR" (id=1)
            if resultado and resultado[0]['total'] > 0:
                query_reasignar = """
                    UPDATE trabajadores 
                    SET departamento_id = 1 
                    WHERE departamento_id = %s
                """
                _, error = self.query_executor.ejecutar(query_reasignar, (id_departamento,))
                
                if error:
                    return False, f"Error al reasignar trabajadores: {error}"
            
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
